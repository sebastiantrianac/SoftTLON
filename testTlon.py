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
import threading
import time

global numresults
numresults=0

def saltedHash(psw):
    import hashlib
    import binascii
    print("Hashing {}".format(psw))
    dk = hashlib.pbkdf2_hmac('sha256', psw, 'salt', 100000)
    return binascii.hexlify(dk)

def GetWords(N):
    a_file = open("test/WordList.txt", "r")
    list_of_words = []
    for line in a_file:
        stripped_line = line.strip()
        #line_list = stripped_line.split()
        list_of_words.append(stripped_line)
    a_file.close()
    set = []
    while(len(set)<N):
        set += (list_of_words[0:N-len(set)])
    return set[0:N]


class StoppableThread(threading.Thread):
    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
    def stop(self):
        self._stop_event.set()
    def stopped(self):
        return self._stop_event.is_set()

class MonitorThread(StoppableThread):
    def run(self):
        prevnumres = 0
        t0 = int(time.time())
        global numres
        global dnumres
        while(not self.stopped()):
            #print man.numresults
            t = int(time.time()) - t0
            tmp =man.numresults
            numres.append((t,tmp))
            dnumres.append((t,tmp-prevnumres))
            prevnumres = tmp
            time.sleep(1)
    
#def GetWords(N):
#    import urllib2
#    word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
#    response = urllib2.urlopen(word_site)
#    txt = response.read()
#    WORDS = txt.splitlines()
#    return WORDS[0:N]

class HaltException(Exception): pass

if __name__ == '__main__':
    try:
        if len(sys.argv) > 1 and sys.argv[1] == 'producer':
            man.tlon_parallelize('192.168.65.1',saltedHash, GetWords(503))
        else:
            man.runclient('192.168.1.100', int(sys.argv[2]))
        raise HaltException("")

    except HaltException as h:
        print(h)
        # now what?
        
numres=[]
dnumres=[]
man.numresults = 0
p = MonitorThread()
p.start()
man.tlon_parallelize('192.168.1.100',saltedHash, GetWords(100000))

p.stop()
import matplotlib.pyplot as plt
import numpy as np
fig, axs = plt.subplots(nrows=2, ncols=1,figsize=(8, 8),sharex=True)
plt.setp(axs[-1], xlabel='Time (S)',ylabel='Throughput (Res)')
xs=[x[0] for x in numres]
ys=[x[1] for x in numres]
axs[0].plot(xs,ys)
axs[0].set_title('Responses x Time')
axs[0].set_ylim(-10, axs[0].get_ylim()[1]*1.1)
xs=[x[0] for x in dnumres]
ys=[x[1] for x in dnumres]
axs[1].scatter(xs,ys)
#axs[1].plot(dnumres,'g.')
z = np.polyfit(xs, ys, 1)
trend = np.poly1d(z)
axs[1].plot(xs,trend(xs),"r--")
axs[1].set_title('Change on Responses x Time')
axs[1].set_ylim(-10, axs[1].get_ylim()[1]*1.1)
plt.show()

plt.savefig('common_labels_text.png', dpi=300)

import sys
import MultiPManager.distProc as man
man.runclient('192.168.1.100', 1)



for i in range(10):
    y = np.random.random()
    plt.plot(i, y)
    plt.pause(0.05)