# Dictionary creation library
# Copyright (C) 2002 John Goerzen
# <jgoerzen@complete.org>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import sys, string, gzip

b64_list = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
url_headword = "00-database-url"
short_headword = "00-database-short"
info_headword = "00-database-info"


def b64_encode(val):
    """Takes as input an integer val and returns a string of it encoded
    with the base64 algorithm used by dict indexes."""
    startfound = 0
    retval = ""
    for i in range(5, -1, -1):
        thispart = (val >> (6 * i)) & ((2 ** 6) - 1)
        if (not startfound) and (not thispart):
            # Both zero -- keep going.
            continue
        startfound = 1
        retval += b64_list[thispart]
    if len(retval):
        return retval
    else:
        return b64_list[0]
    
def b64_decode(str):
    """Takes as input a string and returns an integer value of it decoded
    with the base64 algorithm used by dict indexes."""
    if not len(str):
        return 0
    retval = 0
    shiftval = 0
    for i in range(len(str) - 1, -1, -1):
        val = b64_list.index(str[i])
        retval = retval | (val << shiftval)
        shiftval += 6
    return retval

validdict = {}
for x in string.ascii_letters + string.digits + " \t":
    validdict[x] = 1

def sortnormalize(x):
    """Returns a value such that x is mapped to a format that sorts properly
    with standard comparison."""
    x2 = ''
    for i in range(len(x)):
        if validdict.has_key(x[i]):
            x2 += x[i]
    return x2.upper() + "\0" + x.upper()

def sortfunc(x, y):
   """Emulate sort -df."""
   xl = x.split("\0")
   yl = y.split("\0")
   ret = cmp(xl[0], yl[0])
   if ret != 0:
       return ret
   return cmp(xl[1], yl[1])

class DictWriter:
    def __init__(self, basename, url = 'unknown', shortname = 'unknown',
                 longinfo = 'unknown', quiet = 0):
        """Initialize a DictWriter object.  Will create 'basename.dict' and
        'basename.index' files.  url, shortname, and longinfo specify the
        respective attributes of the database.  If quiet is 1,
        status messages are not printed."""
        self.dictfile = open(basename + ".dict", "wb")
        self.indexfile = open(basename + ".index", "wb")
        self.indexentries = {}
        self.count = 0
        self.quiet = quiet
        self.writeentry(url_headword + "\n     " + url, [url_headword])
        self.writeentry(short_headword + "\n     " + shortname,
                        [short_headword])
        self.writeentry(info_headword + "\n" + longinfo, [info_headword])

    def update(self, string):
        """Writes string out, if not quiet."""
        if not self.quiet:
            sys.stdout.write(string)
            sys.stdout.flush()

    def writeentry(self, defstr, headwords):
        """Writes an entry.  defstr holds the content of the definition.
        headwords is a list specifying one or more words under which this
        definition should be indexed.  This function always adds \n
        to the end of defstr."""
        start = self.dictfile.tell()
        defstr += "\n"
        self.dictfile.write(defstr)
        for word in headwords:
            if not self.indexentries.has_key(word):
                self.indexentries[word] = []
            self.indexentries[word].append([start, len(defstr)])
            self.count += 1

        if self.count % 1000 == 0:
            self.update("Processed %d records\r" % self.count)

    def finish(self, dosort = 1):
        """Called to finish the writing process.  **REQUIRED**.
        This will write the index and close the files.

        dosort is optional and defaults to true.  If set to false,
        dictlib will not sort the index file.  In this case, you
        MUST manually sort it through "sort -df" before it can be used.
        You might want to do this if you have a very large file since
        dictdlib's sort algorithm is not very efficient yet."""


        self.update("Processed %d records.\n" % self.count)

        if dosort:
            self.update("Sorting index: converting")

            indexlist = []
            for word, defs in self.indexentries.items():
                for thisdef in defs:
                    indexlist.append("%s\t%s\t%s" % (word, b64_encode(defs[0]),
                                                     b64_encode(defs[1])))

            self.update(" mapping")
                
            sortmap = {}
            for entry in indexlist:
                norm = sortnormalize(entry)
                if sortmap.has_key(norm):
                    sortmap[norm].append(entry)
                    sortmap[norm].sort(sortfunc)
                else:
                    sortmap[norm] = [entry]

            self.update(" listing")
                
            normalizedentries = sortmap.keys()

            self.update(" sorting")

            normalizedentries.sort()

            self.update(" re-mapping")
            indexlist = []

            for normentry in normalizedentries:
                for entry in sortmap[normentry]:
                    indexlist.append(entry)

            self.update(", done.\n")

        self.update("Writing index...\n")
            
        for entry in indexlist:
            self.indexfile.write(entry + "\n")

        self.indexfile.close()
        self.dictfile.close()

        self.update("Complete.\n")

class DictReader:
    def __init__(self, basename):
        """Initialize a DictReader object.  Provide it with the basename."""
        self.basename = basename
        try:
            self.dictfile = open(self.basename + ".dict", "rb")
        except IOError:
            self.dictfile = gzip.GzipFile(self.basename + ".dict.dz", "rb")
        self.indexfile = open(self.basename + ".index", "rt")

    def getdeflist(self):
        """Returns a list of strings naming all definitions contained
        in this dictionary."""
        self.indexfile.seek(0)
        retval = []
        for line in self.indexfile.xreadlines():
            splits = line.split("\t")
            retval.append(splits[0])
        return retval

    def getdef(self, defname):
        """Given a definition name, returns a list of strings
        with all matching definitions."""
        retval = []
        self.indexfile.seek(0)
        for line in self.indexfile.xreadlines():
            word, start, size = line.rstrip().split("\t")
            if not word == defname:
                continue
            start = b64_decode(start)
            size = b64_decode(size)
            self.dictfile.seek(start)
            retval.append(self.dictfile.read(size))
        return retval
    
