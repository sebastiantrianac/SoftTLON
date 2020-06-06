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
import stomp
import dill as pickle
import MultiPManager.managerImp as managerImp
import MultiPManager.multiProc as multiProc

AUTHKEY = ''

tlon_resources = {}

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
        #print('Received a message {}'.format(message))
        print('Request for resource {}'.format(message))
        if sys.version_info[0]<3:
            tmp = pickle.loads(message)
        else:
            tmp = pickle.loads(message.encode())
        tlon_resources[tmp.__name__] = tmp


class __ordersTopicListener__(stomp.ConnectionListener):
    def on_error(self, headers, message):
        print('Received an error {}'.format(message))

    def on_message(self, headers, message):
        global tlon_resources
        if sys.version_info[0]<3:
            tmp = pickle.loads(message)
        else:
            tmp = pickle.loads(message.encode())
        print("{},{},{}".format(tmp['ip'], tmp['portnum'], tmp['authkey']))
        print(tmp)
        if tmp['resourceName'] in tlon_resources:
            manager = managerImp.make_client_manager(tmp['ip'], tmp['portnum'], tmp['authkey'])
            job_q = manager.get_job_q()
            result_q = manager.get_result_q()
            multiProc.tlon_multiprocessing(job_q, result_q, tlon_resources[tmp['resourceName']])
