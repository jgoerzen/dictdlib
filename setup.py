#!/usr/bin/env python2.2

# $Id: setup.py,v 1.6 2002/06/11 20:07:12 jgoerzen Exp $

# Python API for generating dict files.
# COPYRIGHT #
# Copyright (C) 2002 John Goerzen
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
# END OF COPYRIGHT #


from distutils.core import setup

setup(name = "dictdlib",
      version = "2.0.2",
      description = "Python library for generating dictd files",
      author = "John Goerzen",
      author_email = 'jgoerzen@complete.org',
      url = 'gopher://quux.org/1/devel/dictdlib',
      py_modules = ['dictdlib'],
      license = "GPL version 2"
)

