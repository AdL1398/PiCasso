
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
from monitoringManager_thread import MonitoringThread
from decisionEngine_thread import DecisionEngine_Thread
from threading import Timer, Thread, Event
import sys
import traceback
import os
import time

class ServiceManager(object):
    def __init__(self):
        self.namePrefix1 = '/picasso/monitoring/SEG_1/'
        self.namePrefix2 = '/picasso/monitoring/SEG_2/'
        self.namePrefix_DE = '/picasso/service_deployment/'
        self.monitoring_frequency = 10

    def run(self):
        try:
            #instantiate DB here
            #print 'Instantiate monitoring DB'
            #os.system("docker run -p 8086:8086 -d -v /home/adisorn/influxdb:/var/lib/influxdb influxdb:alpine")
            #instantiate Grafana
            # Create Thread
            # stopFlag = Event()
            # print 'Start Monitoring Manager'
            # SEG1_monitoring = MonitoringThread(1, "Monitoring-Thread-1", 1, self.namePrefix1, stopFlag, self.monitoring_frequency)
            # SEG1_monitoring.start()

            print 'Start Decision Engine'
            Decision_engine = DecisionEngine_Thread(2, "DecisionEngine-Thread", self.namePrefix_DE)
            Decision_engine.start()

        except RuntimeError as e:
            print "ERROR: %s" %  e

        return True

if __name__ == '__main__':

    #nameInput  = raw_input('Enter Name of Content ')
    print 'Start Service Manager'
    try:
        ServiceManager().run()
    except:
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)
