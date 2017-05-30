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
from termopi import termopi # class with dictionary data structure

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
        content_type = self.DataStore[str(interestName)]['Type']
        print "content type: %s" %content_type
        content = self.DataStore[str(interestName)]['Content']
        if content_type == 'text':
            print "attach text to Data message"
            print "Content: %s" %content
            data.setContent(content)
            hourMilliseconds = 600 * 1000
            data.getMetaInfo().setFreshnessPeriod(hourMilliseconds)
            self.keyChain.sign(data, self.keyChain.getDefaultCertificateName())
            face.send(data.wireEncode().toBuffer())
            print "Replied to Interest name: %s" % interestName.toUri()
            print "Replied with Data name: %s" % interestName.toUri()

        elif content_type == 'file':
            print "chop file to small piece of chunks"
            pass
        elif content_type == 'function':
            print "call other functions to get Data"
            monitoring_agent = termopi()
            if content == 'monitoring':
                print "Check Pi and Containers Status"
                monitoring_agent.prt_pi_resources()
                print "Update json file"
                monitoring_agent.create_jsonfile_with_pi_status()
                try:
            # due to overhead of NDN name and other header values; NDN header overhead + Data packet content = < maxNdnPacketSize
            # So Here segment size is hard coded to 5000 KB.
            # Class Enumerate publisher is used to split large files into segments and get a required segment ( segment numbers started from 0)
                dataSegment, last_segment_num = EnumeratePublisher(jsonfileName, 8000, SegmentNum).getFileSegment()
            # create the DATA name appending the segment number
                dataName = dataName.appendSegment(SegmentNum)
                data = Data(dataName)
                data.setContent(dataSegment)
            # set the final block ID to the last segment number
                last_segment = (Name.Component()).fromNumber(last_segment_num)
                data.getMetaInfo().setFinalBlockId(last_segment)
                hourMilliseconds = 600 * 1000
                data.getMetaInfo().setFreshnessPeriod(hourMilliseconds)
            # currently Data is signed from the Default Identitiy certificate
                self.keyChain.sign(data, self.keyChain.getDefaultCertificateName())
            # Sending Data message
                face.send(data.wireEncode().toBuffer())
                print "Replied to Interest name: %s" % interestName.toUri()
                print "Replied with Data name: %s" % dataName.toUri()
                pass

        else:
            print "content type is mismatch"
            pass
    def onRegisterFailed(self, prefix):
        print "Register failed for prefix", prefix.toUri()
        self.isDone = True
