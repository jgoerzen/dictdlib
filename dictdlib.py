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

import sys, string

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
for x in string.ascii_letters + string.digits + ' ':
    validdict[x] = 1

def sortfunc(x, y):
    """Used to sort entries according to the format required for the index."""
    x2 = ''
    for char in x:
        if validdict.has_key(char):
            x2 += char
    for char in y:
        if validdict.has_key(char):
            y2 += char

    return cmp(x2.lower(), y2.lower())

class DictWriter:
    def __init__(self, basename, url = 'unknown', shortname = 'unknown',
                 longinfo = 'unknown', quiet = 0):
        """Initialize a DictWriter object.  Will create 'basename.dict' and
        'basename.index' files.  url, shortname, and longinfo specify the
        respective attributes of the database.  If quiet is 1,
        status messages are not printed."""
        self.dictfile = open(basename + ".dict", "wb")
        self.indexfile = open(basename + ".index", "wb")
        self.indexentries = []
        self.count = 0
        self.quiet = quiet
        self.writeentry(url_headword + "\n     " + url, [url_headword])
        self.writeentry(short_headword + "\n     " + shortname,
                        [short_headword])
        self.writeentry(info_headword + longinfo, [info_headword])

    def writeentry(self, defstr, headwords):
        """Writes an entry.  defstr holds the content of the definition.
        headwords is a list specifying one or more words under which this
        definition should be indexed."""
        start = self.dictfile.tell()
        defstr += "\n"
        self.dictfile.write(defstr)
        for word in headwords:
            self.indexentries.append("%s\t%s\t%s" % \
                                     (word, b64_encode(start),
                                      b64_encode(len(defstr))))
            self.count += 1

        if (not self.quiet) and (self.count % 1000 == 0):
            sys.stdout.write("Processed %d records\r" % self.count)
            sys.stdout.flush()

    def finish(self):
        """Called to finish the writing process.  **REQUIRED**.
        This will write the index and close the files."""
        if not self.quiet:
            sys.stdout.write("\nProcessed %d records.\nWriting index..." % \
                             self.count)
            sys.stdout.flush()

        self.indexentries.sort()
        for entry in self.indexentries:
            self.indexfile.write(entry + "\n")

        self.indexfile.close()
        self.dictfile.close()

        if not self.quiet:
            sys.stdout.write(" Finished.\n")
