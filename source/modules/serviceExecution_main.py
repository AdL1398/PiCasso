"""
title           : serviceExecution_main.py
description     : includes
                  a) register name prefix
                  b) response Interest messages which have matching name prefixes
source          :
author          : Adisorn Lertsinsrubtavee
date            : 27 June 2017
version         : 1.0
contributors    :
usage           :
notes           :
compile and run : It is a python module imported by a main python programme.
python_version  : Python 2.7.12
====================================================
"""

import sys
import time
import argparse
import traceback
import threading
import os
import dockerctl
from pyndn import Interest
from pyndn import Data
from pyndn import Exclude
from pyndn import Name
from pyndn import Face
from pyndn import InterestFilter
from pyndn.security import KeyChain
from pprint import pprint
from termopi import termopi # class with dictionary data structure
from enumerate_publisher import EnumeratePublisher

class ServiceExecution(object):
    def __init__(self, producerName, namePrefix):
        self.configPrefix = Name(namePrefix)
        self.outstanding = dict()
        self.isDone = False
        self.keyChain = KeyChain()
        self.face = Face("127.0.0.1")
        self.script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
        self.script_dir = os.path.split(self.script_path)[0] #i.e. /path/to/dir/
        self.Datamessage_size = 8000 #8kB --> Max Size from NDN standard
        self.producerName = producerName

    def run(self):
        try:
            self.face.setCommandSigningInfo(self.keyChain, self.keyChain.getDefaultCertificateName())
            self.face.registerPrefix(self.configPrefix, self.onInterest, self.onRegisterFailed)
            print "Registered prefix : " + self.configPrefix.toUri()

            while not self.isDone:
                self.face.processEvents()
                time.sleep(0.01)

        except RuntimeError as e:
            print "ERROR: %s" %  e

    def onInterest(self, prefix, interest, face, interestFilterId, filter):
        interestName = interest.getName()
        print "Interest Name: %s" %interestName
        interest_name_components = interestName.toUri().split("/")
        if "service_deployment" in interest_name_components:
            print 'Start service deployment'
            ## check image is running or not
            #Ger info from serviceInfo
            serviceName = 'web-uhttpd'
            if dockerctl.deployContainer(serviceName) == False:
                print 'Service: %s is not locally cached, pull from Repo' % serviceName
                #print 'Sending Interest message: %s' % prefix.requestService
                #self.sendNextInterest(prefix.requestService)
        else:
            print "Interest name mismatch"

    def onRegisterFailed(self, prefix):
        print "Register failed for prefix", prefix.toUri()
        self.isDone = True
