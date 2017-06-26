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
import os
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

class Monitoring_Agent(object):
    def __init__(self, namePrefix, producerName):
        self.configPrefix = Name(namePrefix)
        self.outstanding = dict()
        self.isDone = False
        self.keyChain = KeyChain()
        self.face = Face("127.0.0.1")
        #self.DataStore = DS.readDataStore_json()
        #self.DataStore = DS.table
        self.script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
        self.script_dir = os.path.split(self.script_path)[0] #i.e. /path/to/dir/
        self.Datamessage_size = 8000 #8kB --> Max Size from NDN standard
        self.producerName = producerName
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
        #print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        #pprint(self.DataStore)
        print "Interest Name: %s" %interestName
        interest_name_components = interestName.toUri().split("/")
        if "monitoring" in interest_name_components:
            print "Check Pi and Containers Status"
            monitoring_agent = termopi()
            monitoring_agent.prt_pi_resources()
            print "Update json file"
            filename = "piStatus"+self.producerName+".json"
            folder_name = "PIstatus/"
            rel_path = os.path.join(self.script_dir, folder_name)
            if not os.path.exists(rel_path):
                os.makedirs(rel_path)
            abs_file_path = os.path.join(rel_path, filename)
            monitoring_agent.create_jsonfile_with_pi_status(abs_file_path)
            freshness = 10 #milli second, content will be deleted from the cache after freshness period
            self.sendingFile(abs_file_path, interest, face, freshness)
        else:
            print "Interest name mismatch"
    # def onInterest(self, prefix, interest, face, interestFilterId, filter):
    #
    #     interestName = interest.getName()
    #     data = Data(interestName)
    #     print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    #     pprint(self.DataStore)
    #     print "Interest Name: %s" %interestName
    #     content_type = self.DataStore[str(interestName)]['Type']
    #     print "content type: %s" %content_type
    #     content = self.DataStore[str(interestName)]['Content']
    #     if content_type == 'text':
    #         print "attach text to Data message"
    #         print "Content: %s" %content
    #         data.setContent(content)
    #         hourMilliseconds = 600 * 1000
    #         data.getMetaInfo().setFreshnessPeriod(hourMilliseconds)
    #         self.keyChain.sign(data, self.keyChain.getDefaultCertificateName())
    #         face.send(data.wireEncode().toBuffer())
    #         print "Replied to Interest name: %s" % interestName.toUri()
    #         print "Replied with Data name: %s" % interestName.toUri()
    #
    #     elif content_type == 'file':
    #         print "chop file to small piece of chunks"
    #         pass
    #     elif content_type == 'function':
    #         print "call other functions to get Data"
    #
    #         if content == 'monitoring':
    #             print "Check Pi and Containers Status"
    #             monitoring_agent = termopi()
    #             monitoring_agent.prt_pi_resources()
    #             print "Update json file"
    #             filename = "piStatus"+self.producerName+".json"
    #             folder_name = "PIstatus/"
    #             rel_path = os.path.join(self.script_dir, folder_name)
    #             if not os.path.exists(rel_path):
    #                 os.makedirs(rel_path)
    #             abs_file_path = os.path.join(rel_path, filename)
    #             f = os.popen('date +%s')
    #             #timestamp = f.read()
    #             filename = "piStatus_"+self.producerName+".json"
    #             #rel_path = "PIstatus/"+filename
    #             #abs_file_path = os.path.join(self.script_dir, rel_path)
    #             #print "File path of monitoring Pi:%s" %abs_file_path
    #             monitoring_agent.create_jsonfile_with_pi_status(abs_file_path)
    #             freshness = 10 #milli second
    #             self.sendingFile(abs_file_path, interest, face, freshness)
    #     else:
    #         print "content type is mismatch"
    #         pass
    def onRegisterFailed(self, prefix):
        print "Register failed for prefix", prefix.toUri()
        self.isDone = True

    def sendingFile(self, file_path, interest, face, freshness):
        print "Sending File Function"
        interestName = interest.getName()
        interestNameSize = interestName.size()
        #interest_name_components = interestName.toUri().split("/")
        #timeStamp = interest_name_components[interest_name_components.index("service_monitoring") + 2]
        #print "Receive Interest message name: %s" % interestName
        ##### V2 Data message is JSON file
        try:
            SegmentNum = (interestName.get(interestNameSize - 1)).toSegment()
            dataName = interestName.getSubName(0, interestNameSize - 1)

        # If no segment number is included in the INTEREST, set the segment number as 0 and set the file name to configuration script to be sent
        except RuntimeError as e:
            SegmentNum = 0
            dataName = interestName
        # Put file to the Data message
        try:
            # due to overhead of NDN name and other header values; NDN header overhead + Data packet content = < maxNdnPacketSize
            # So Here segment size is hard coded to 5000 KB.
            # Class Enumerate publisher is used to split large files into segments and get a required segment ( segment numbers started from 0)
            dataSegment, last_segment_num = EnumeratePublisher(file_path, self.Datamessage_size, SegmentNum).getFileSegment()
            # create the DATA name appending the segment number
            dataName = dataName.appendSegment(SegmentNum)
            data = Data(dataName)
            data.setContent(dataSegment)

            # set the final block ID to the last segment number
            last_segment = (Name.Component()).fromNumber(last_segment_num)
            data.getMetaInfo().setFinalBlockId(last_segment)
            #hourMilliseconds = 600 * 1000
            data.getMetaInfo().setFreshnessPeriod(freshness)

            # currently Data is signed from the Default Identitiy certificate
            self.keyChain.sign(data, self.keyChain.getDefaultCertificateName())
            # Sending Data message
            face.send(data.wireEncode().toBuffer())
            print "Replied to Interest name: %s" % interestName.toUri()
            print "Replied with Data name: %s" % dataName.toUri()

            # If configuration manager has sent the last segment of the file, script can be stopped.
            # if SegmentNum == last_segment_num:
            # self.isDone = True

        except ValueError as err:
            print "ERROR: %s" % err

