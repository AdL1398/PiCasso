
"""
title           : serviceManger.py
description     : This class operates as Service Manager in PiCasso Architecture. It provides following functions:
                  a) instantiate Monitoring DB (InfluxDB container)
                  b) instantiate Monitoring web interface (grafana container)
                  c) create thread for monitoring Manager to fetch data from SEG
source          :
author          : Adisorn Lertsinsrubtavee
date            : 22 June 2017
version         : 1.0
contributors    :
usage           :
notes           :
compile and run : It is a python module imported by a main python programme.
python_version  : Python 2.7.12
====================================================
"""
from monitoringThread import MonitoringThread
from threading import Timer, Thread, Event
import sys
import traceback
import os
import time

class ServiceManaer(object):
    def __init__(self):
        self.namePrefix1 = '/picasso/monitoring/SEG_1/'
        self.namePrefix2 = '/picasso/monitoring/SEG_2/'
        self.monitoring_frequency = 10

    def run(self):
        try:
            #instantiate DB here
            print 'Instantiate monitoring DB'
            os.system("docker run -p 8086:8086 -d -v /home/adisorn/influxdb:/var/lib/influxdb influxdb:alpine")
            #instantiate Grafana
            # Create Thread
            stopFlag = Event()
            print 'Start Monitoring Manager'
            thread1 = MonitoringThread(1, "Thread-1", 1, self.namePrefix1, stopFlag, self.monitoring_frequency)
            thread1.start()

        except RuntimeError as e:
            print "ERROR: %s" %  e

        return True

if __name__ == '__main__':

    #nameInput  = raw_input('Enter Name of Content ')
    print 'Start Service Manager'
    try:
        ServiceManaer().run()
    except:
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)
