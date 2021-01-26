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

import sys
import threading
import time
from collections import Mapping, Container
from sys import getsizeof
from guppy import hpy
import psutil
import platform
from datetime import datetime
import socket

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
        hp=hpy()
        t0 = int(time.time())
        global numres
        global dnumres
        hp.heap()
        while(not self.stopped()):
            #print man.numresults
            t = int(time.time()) - t0
            tmp =man.numresults
            numres.append((t,tmp))
            dnumres.append((t,tmp-prevnumres))
            prevnumres = tmp
            time.sleep(1)
        hp.heap()
        
 
def deep_getsizeof(o, ids):
    d = deep_getsizeof
    if id(o) in ids:
        return 0
    r = getsizeof(o)
    ids.add(id(o))
    if isinstance(o, str) or isinstance(0, unicode):
        return r
    if isinstance(o, Mapping):
        return r + sum(d(k, ids) + d(v, ids) for k, v in o.iteritems())
    if isinstance(o, Container):
        return r + sum(d(x, ids) for x in o)
    return r 

platform = platform.uname()

cpufreq = psutil.cpu_freq()

cpu={
	'phcores':psutil.cpu_count(logical=False),
	'cores':psutil.cpu_count(logical=True),
	'freqMax':cpufreq.max,
	'freqMin':cpufreq.min,
	'freqCur':cpufreq.current,
	'usage':psutil.cpu_percent()
}

svmem = psutil.virtual_memory()

memory={
	'total':    round(svmem.total/1000000000.0,2),
	'available':round(svmem.available/1000000000.0,2),
	'used':     round(svmem.used/1000000000.0,2),
	'percent':  svmem.percent
}
	
nodeDesc = {
			'node':socket.gethostbyname(socket.gethostname()),
			'platform':platform,
			'cpu':cpu,
			'memory':memory
			}
