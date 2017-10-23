
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
import os
import sys
import time
import traceback
from threading import Timer, Thread, Event

from modules.DecisionEngine.decisionEngine_thread import Decision_Engine
from modules.Monitoring.monitoringManager_thread import Monitoring_Manager
from modules.ServiceRepo.serviceRepo_thread import Service_Repo


class ServiceManager(object):
    def __init__(self):
        self.namePrefix1 = '/picasso/monitoring/SEG_1/'
        self.namePrefix2 = '/picasso/monitoring/SEG_2/'
        self.namePrefix3 = '/picasso/monitoring/SEG_3/'
        self.namePrefix_DE = '/picasso/service_deployment_pull/'
        self.monitoring_frequency = 10

    def run(self):
        try:
            #instantiate DB here
            print 'Instantiate monitoring DB'
            os.system("docker rm -f $(docker ps -a -q)")
            os.system("docker run -p 8086:8086 -d -v /home/adisorn/influxdb:/var/lib/influxdb --name influxdb influxdb:alpine")
            #instantiate Grafana
            os.system("docker run -d -p 3000:3000 --link influxdb --name grafana grafana/grafana")
            #Create Thread
            stopFlag = Event()
            print 'Start Monitoring Manager'
            #SEG1_monitoring = Monitoring_Manager(1, "Monitoring-Thread-1", 1, self.namePrefix1, stopFlag, self.monitoring_frequency)
            #SEG1_monitoring.start()

            SEG2_monitoring = Monitoring_Manager(2, "Monitoring-Thread-2", 1, self.namePrefix2, stopFlag, self.monitoring_frequency)
            SEG2_monitoring.start()

            #SEG3_monitoring = MonitoringThread_Manager(3, "Monitoring-Thread-3", 1, self.namePrefix3, stopFlag, self.monitoring_frequency)
            #SEG3_monitoring.start()

            # print 'Start Decision Engine'
            DE = Decision_Engine(4, "DecisionEngine-Thread", self.namePrefix_DE)
            DE.start()

            #ServiceRepo = Service_Repo(5, "ServiceRepo-Thread", 2200)
            #ServiceRepo.start()

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
