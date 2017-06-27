"""
title           : decisionEngine_main.py
description     : This class operates as decision engine. It includes following functions:
                  a) open a NDN face for name:/picasso/service_deployment
                  b)


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
from pyndn import Name
from pyndn import Data
from pyndn import Face
from pyndn import InterestFilter
from pyndn.security import KeyChain
from pyndn import Interest
import dockerctl
import os
import time
from enumerate_publisher import EnumeratePublisher


class DecisionEngine(object):
    def __init__(self, namePrefix):
        self.outstanding = dict()
        self.isDone = False
        self.keyChain = KeyChain()
        self.face = Face("127.0.0.1")
        self.configPrefix = Name(namePrefix)
        self.script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
        self.script_dir = os.path.split(self.script_path)[0] #i.e. /path/to/dir/
        folder_name = "SC_repository/"
        rel_path = os.path.join(self.script_dir, folder_name)
        if not os.path.exists(rel_path):
            os.makedirs(rel_path)

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

        return True

    def onInterest(self, prefix, interest, face, interestFilterId, filter):
        interestName = interest.getName()
        print "Interest Name: %s" %interestName
        interest_name_components = interestName.toUri().split("/")

        if "service_deployment" in interest_name_components:
            print 'Query database'
            print 'Call decision engine algorithm'
            print 'Start service deployment'
        else:
            print "Interest name mismatch"

    def onRegisterFailed(self, prefix):
        print "Register failed for prefix", prefix.toUri()
        self.isDone = True
