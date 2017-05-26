"""
title           : producer.py
description     : includes
                  a) register name prefix
                  b) response Interest messages which have matching name prefixes
source          :
author          : Adisorn Lertsinsrubtavee
date            : 19 May 2017
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
from pyndn import Interest
from pyndn import Data
from pyndn import Exclude
from pyndn import Name
from pyndn import Face
from pyndn import InterestFilter
from pyndn.security import KeyChain
from pprint import pprint

class Producer(object):
    def __init__(self, namePrefix, DS):
        self.configPrefix = Name(namePrefix)
        self.outstanding = dict()
        self.isDone = False
        self.keyChain = KeyChain()
        self.face = Face("127.0.0.1")
        self.DataStore = DS.readDataStore_json()
        #print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        #pprint(self.DataStore)

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
        data = Data(interestName)
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        pprint(self.DataStore)
        print "Interest Name: %s" %interestName
        content = self.DataStore[str(interestName)]['Content']
        print "Content: %s" %content
        data.setContent(content)
        hourMilliseconds = 600 * 1000
        data.getMetaInfo().setFreshnessPeriod(hourMilliseconds)
        self.keyChain.sign(data, self.keyChain.getDefaultCertificateName())
        face.send(data.wireEncode().toBuffer())
        print "Replied to Interest name: %s" % interestName.toUri()
        print "Replied with Data name: %s" % interestName.toUri()

    def onRegisterFailed(self, prefix):
        print "Register failed for prefix", prefix.toUri()
        self.isDone = True
