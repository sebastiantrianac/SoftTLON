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

import multiprocessing
import Queue


nprocs = 2

def setThreads (threads):
    global nprocs
    nprocs = threads

def tlon_threading(job_q, result_q, routine):
    myname = multiprocessing.current_process().name
    outdict = {}
    while True:
        try:
            job = job_q.get_nowait()
            print '%s got %s nums...' % (myname, len(job))
            for n in job:
                # outdict.append(routine(n))
                outdict[n] = routine(n)
            # outdict = {n: routine(n) for n in job}
            result_q.put(outdict)
            print '  %s done' % myname
        except Queue.Empty:
            return


def tlon_multiprocessing(shared_job_q, shared_result_q, routine):
    procs = []
    for i in range(nprocs):
        p = multiprocessing.Process(
            target=tlon_threading,
            args=(shared_job_q, shared_result_q, routine))
        procs.append(p)
        p.start()

    for p in procs:
        p.join()
