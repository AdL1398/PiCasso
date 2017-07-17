"""
title           : decisionEngine_thread.py
description     : This class manages a thread for decision engine. It opens the thread to wait for Interest name:
                  /picasso/service_deployment
source          :
author          : Adisorn Lertsinsrubtavee
date            : 25 June 2017
version         : 1.0
contributors    :
usage           :
notes           :
compile and run : It is a python module imported by a main python programme.
python_version  : Python 2.7.12
====================================================
"""

import threading
from decisionEngine_main import Decision_Engine_Main

class Decision_Engine (threading.Thread):
   def __init__(self, threadID, threadName, namePrefix):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.threadname = threadName
      self.namePrefix = namePrefix

   def run(self):
      print "Starting " + self.threadname
      decision_engine = Decision_Engine_Main(self.namePrefix)
      decision_engine.run()
      print "Exiting " + self.threadname
