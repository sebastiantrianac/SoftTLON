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
from multiprocessing.managers import SyncManager
import Queue
import sys
import stomp
import dill as pickle
import time

IP = '192.168.0.8'
MANAGER_PORTNUM = 9999
BROKER_PORTNUM = 61613
AUTHKEY = ''
THREADS = 2

tlon_resources = {}

def make_server_manager(port, authkey):
    job_q = Queue.Queue()
    result_q = Queue.Queue()

    class JobQueueManager(SyncManager):
        pass

    JobQueueManager.register('get_job_q', callable=lambda: job_q)
    JobQueueManager.register('get_result_q', callable=lambda: result_q)

    manager = JobQueueManager(address=('', port), authkey=authkey)
    manager.start()
    # print 'Server started at port %s' % port
    return manager


def make_client_manager(ip, port, authkey):
    class ServerQueueManager(SyncManager):
        pass

    ServerQueueManager.register('get_job_q')
    ServerQueueManager.register('get_result_q')

    manager = ServerQueueManager(address=(ip, port), authkey=authkey)
    manager.connect()

    print 'Client connected to %s:%s' % (ip, port)
    return manager


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


def tlon_multiprocessing(shared_job_q, shared_result_q, routine, nprocs):
    procs = []
    for i in range(nprocs):
        p = multiprocessing.Process(
            target=tlon_threading,
            args=(shared_job_q, shared_result_q, routine))
        procs.append(p)
        p.start()

    for p in procs:
        p.join()


def make_nums(N):
    nums = [9999]
    for i in xrange(N):
        nums.append(nums[-1] + 2)
    return nums


def BrokerConnect(ip, port):
    conn = stomp.Connection([(ip, port)])
    conn.start()
    conn.connect(wait=True)
    return conn


class __resourceTopicListener__(stomp.ConnectionListener):
    def on_error(self, headers, message):
        print('Received an error {}'.format(message))

    def on_message(self, headers, message):
        global tlon_resources
        tmp = pickle.loads(message)
        tlon_resources[tmp.__name__] = tmp


class __ordersTopicListener__(stomp.ConnectionListener):
    def on_error(self, headers, message):
        print('Received an error {}'.format(message))

    def on_message(self, headers, message):
        global tlon_resources
        tmp = pickle.loads(message)
        print("{},{},{}".format(tmp['ip'], tmp['portnum'], tmp['authkey']))
        print tmp
        if tmp['resourceName'] in tlon_resources:
            manager = make_client_manager(tmp['ip'], tmp['portnum'], tmp['authkey'])
            job_q = manager.get_job_q()
            result_q = manager.get_result_q()
            tlon_multiprocessing(job_q, result_q, tlon_resources[tmp['resourceName']], THREADS)


def updateResourceOnSuscribers(resource, conn):
    msg = pickle.dumps(resource)
    conn.send(destination='/topic/TLONResources', body=msg)


def updateOrderOnSuscribers(name, conn):
    tmp = {"resourceName": name, "ip": IP, "portnum": MANAGER_PORTNUM, "authkey": AUTHKEY}
    msg = pickle.dumps(tmp)
    conn.send(destination='/topic/TLONOrders', body=msg)


def tlon_sharedJobs(f, set, chunkSize):
    conn = BrokerConnect(IP, BROKER_PORTNUM)
    updateResourceOnSuscribers(f, conn)

    manager = make_server_manager(MANAGER_PORTNUM, AUTHKEY)
    shared_job_q = manager.get_job_q()
    shared_result_q = manager.get_result_q()
    for i in range(0, len(set), chunkSize):
        print 'Putting chunk {}:{} in queue'.format(i, i + chunkSize)
        shared_job_q.put(set[i:i + chunkSize])
    time.sleep(2)
    updateOrderOnSuscribers(f.__name__, conn)
    return manager, shared_job_q, shared_result_q


def tlon_parallelize(f,set):
    try:
        resultdict = {}
        N = 102
        chunkSize = 10
        # f = factorize_naive
        manager, shared_job_q, shared_result_q = tlon_sharedJobs(f, set, chunkSize)
        numresults = 0
        if 1:
            tlon_multiprocessing(shared_job_q, shared_result_q, f,1)
        while numresults < N:
            outdict = shared_result_q.get()
            resultdict.update(outdict)
            numresults += len(outdict)
            for num, result in outdict.iteritems():
                print("{}({}) = {}".format(f.__name__, num, result))

        print '--- DONE ---'

    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except ValueError:
        print "Could not convert data to an integer."
    finally:
        time.sleep(2)
        manager.shutdown()


def runclient(threads):
    connResources = BrokerConnect(IP, BROKER_PORTNUM)
    connResources.set_listener('ResourceTopic', __resourceTopicListener__())
    connResources.subscribe(destination='/topic/TLONResources', id=1, ack='auto')

    connOrders = BrokerConnect(IP, BROKER_PORTNUM)
    connOrders.set_listener('OrdersTopic', __ordersTopicListener__())
    connOrders.subscribe(destination='/topic/TLONOrders', id=2, ack='auto')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'producer':
        tlon_parallelize(factorize_naive)
    else:
        runclient()
