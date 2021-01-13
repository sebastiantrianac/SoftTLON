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

import sys
import stomp
import dill as pickle
import time
import MultiPManager.managerImp as managerImp
import MultiPManager.brokermq as brokermq
import MultiPManager.multiProc as multiProc
import socket

if sys.version_info[0]<3:
    import Queue
else:
    import queue

IP = '10.203.177.194'
MANAGER_PORTNUM = 9999
BROKER_PORTNUM = 61613
AUTHKEY = ''

global numresults
numresults=0

tlon_resources = {}

def updateResourceOnSuscribers(resource, conn):
    msg = pickle.dumps(resource,0)
    conn.send(destination='/topic/TLONResources', body=msg)


def updateOrderOnSuscribers(name, ip, portnum, authkey,conn):
    tmp = {"resourceName": name, "ip": ip, "portnum": portnum, "authkey": authkey}
    msg = pickle.dumps(tmp,0)
    conn.send(destination='/topic/TLONOrders', body=msg)

def tlon_sharedJobs(f, set, chunkSize):

    manager = managerImp.make_server_manager(MANAGER_PORTNUM, AUTHKEY)
    shared_job_q = manager.get_job_q()
    shared_result_q = manager.get_result_q()
    for i in range(0, len(set), chunkSize):
        print('Putting chunk {}:{} in queue'.format(i, i + chunkSize))
        shared_job_q.put(set[i:i + chunkSize])

    return manager, shared_job_q, shared_result_q


def tlon_parallelize(ipbroker, f, set):
    try:
        resultdict = {}
        N = 102
        chunkSize = 10

        conn = brokermq.BrokerConnect(ipbroker, BROKER_PORTNUM)
        updateResourceOnSuscribers(f, conn)

        manager, shared_job_q, shared_result_q = tlon_sharedJobs(f, set, chunkSize)

        time.sleep(2)
        hostname = socket.gethostname()
        ipsocket = socket.gethostbyname(hostname)
        updateOrderOnSuscribers(f.__name__, ipsocket, MANAGER_PORTNUM, AUTHKEY, conn)
        global numresults
        numresults = 0
        
        #if 1:
        #    multiProc.tlon_multiprocessing(shared_job_q, shared_result_q, f)
        while numresults < len(set):
            outdict = shared_result_q.get()
            #resultdict.update(outdict)
            numresults += len(outdict)
            #updateResourceOnSuscribers(f, conn)
            #for num, result in outdict.iteritems():
                #print("{}({}) = {}".format(f.__name__, num, result))

        print ('End of Task')

    except IOError as e:
        print ("I/O error({0}): {1}".format(e.errno, e.strerror))
    except ValueError:
        print ("Could not convert data to an integer.")
    finally:
        time.sleep(2)
        manager.shutdown()


def runclient(ipbroker, threads):
    # Setting number of threads that are going to attend the request of processing of the network
    multiProc.setThreads(threads)

    # Connecting to TLONResource Topic to receive shared resources
    connResources = brokermq.BrokerConnect(ipbroker, BROKER_PORTNUM)
    connResources.set_listener('ResourceTopic', brokermq.__resourceTopicListener__())
    connResources.subscribe(destination='/topic/TLONResources', id=1, ack='auto')

    # Connecting to TLONOrders Topic to start executed OoW
    connOrders = brokermq.BrokerConnect(ipbroker, BROKER_PORTNUM)
    connOrders.set_listener('OrdersTopic', brokermq.__ordersTopicListener__())
    connOrders.subscribe(destination='/topic/TLONOrders', id=2, ack='auto')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'producer':
        tlon_parallelize()
    else:
        runclient('192.168.0.8', 2)
