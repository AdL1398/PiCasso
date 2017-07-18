"""
title           : serviceREpo_thread.py
description     : This class manages a thread for service Repo at service manager. It calls the serviceRepo_main module 
source          :
author          : Adisorn Lertsinsrubtavee
date            : 18 July 2017
version         : 1.0
contributors    :
usage           :
notes           :
compile and run : It is a python module imported by a main python programme.
python_version  : Python 2.7.12
====================================================
"""
import threading
from serviceRepo_main import Service_Repo_Main

class Service_Repo (threading.Thread):
    def __init__(self, threadID, threadName, port):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadname = threadName
        self.port = port

    def run(self):
        print "Starting " + self.threadname
        Service_Repo = Service_Repo_Main(self.port)
        Service_Repo.run()
        print "Exiting " + self.threadname



