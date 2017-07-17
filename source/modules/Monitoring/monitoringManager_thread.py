"""
title           : monitoringThread.py
description     : This class manages multi-thread of periodic monitoring process. It calls the monitoring manager
                  periodically (monitoring frequency) to send Interest message to a specific SEG (SEG name).
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

from monitoringManager_main import MonitoringManager_Main
import threading


class Monitoring_Manager (threading.Thread):
   def __init__(self, threadID, name, counter, namePrefix, event, monitoring_frequency):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      self.namePrefix = namePrefix
      self.stopped = event
      self.monitoring_frequency = monitoring_frequency

   def run(self):
      print "Starting " + self.name
      stopFlag = False
      while not self.stopped.wait(self.monitoring_frequency):
         print "creating thread for: %s" %self.namePrefix
         # call a function
         monitoringManager = MonitoringManager_Main(self.namePrefix)
         monitoringManager.run()
      print "Exiting " + self.name

