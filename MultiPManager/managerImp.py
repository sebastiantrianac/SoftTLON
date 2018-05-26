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

from multiprocessing.managers import SyncManager
import Queue

def make_server_manager(port, authkey):
    job_q = Queue.Queue()
    result_q = Queue.Queue()

    class JobQueueManager(SyncManager):
        pass

    JobQueueManager.register('get_job_q', callable=lambda: job_q)
    JobQueueManager.register('get_result_q', callable=lambda: result_q)

    manager = JobQueueManager(address=('', port), authkey=authkey)
    manager.start()
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
