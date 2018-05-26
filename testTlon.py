#!/usr/bin/env python
# coding=utf-8
#
# A module for create a multi-agent system over Ad-hoc networks
# Copyright (C) 2017-2018
# Juan Sebastian Triana Correa <justrianaco@unal.edu.co>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].


__author__ = "Juan Sebastian Triana Correa"
__copyright__ = "Copyright 2015, TLON group"
__license__ = "LGPL"
__version__ = "1.2"
__email__ = "justrianaco@unal.edu.co"
__status__ = "Development"

import MultiPManager.distProc as man
import sys

def saltedHash(psw):
    import hashlib
    import binascii
    print("Hashing {}".format(psw))
    dk = hashlib.pbkdf2_hmac('sha256', psw, 'salt', 100000)
    return binascii.hexlify(dk)

def GetWords(N):
    import urllib2
    word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
    response = urllib2.urlopen(word_site)
    txt = response.read()
    WORDS = txt.splitlines()
    return WORDS[0:N]

class HaltException(Exception): pass

if __name__ == '__main__':
    try:
        if len(sys.argv) > 1 and sys.argv[1] == 'producer':
            man.tlon_parallelize('172.25.13.15',saltedHash, GetWords(503))
        else:
            man.runclient('172.25.13.15', int(sys.argv[2]))
        raise HaltException("")

    except HaltException as h:
        print(h)
        # now what?