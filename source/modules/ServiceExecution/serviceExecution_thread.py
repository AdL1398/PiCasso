"""
title           : serviceExecution_thread.py
description     : This class manages a thread for service execution at SEG. It calls the serviceExecution module when it
                  receives the service deployment message from DE.
source          :
author          : Adisorn Lertsinsrubtavee
date            : 27June 2017
version         : 1.0
contributors    :
usage           :
notes           :
compile and run : It is a python module imported by a main python programme.
python_version  : Python 2.7.12
====================================================
"""

from serviceExecution_main import Service_Execution_Main
import threading


class Service_Execution(threading.Thread):
   def __init__(self, threadID, threadName, producerName, namePrefix, ):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.threadname = threadName
      self.namePrefix = namePrefix
      self.producerName = producerName

   def run(self):
      print "Starting " + self.threadname
      service_execution = Service_Execution_Main(self.producerName, self.namePrefix, )
      service_execution.run()
      print "Exiting " + self.threadname

