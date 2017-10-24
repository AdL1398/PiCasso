"""
title           : monitoringManager.py
description     : This class operates as Monitoring manager. It includes following functions:
                  a) send Interest message to fetch monitoring data of selected SEG.
                  b) process Data message received from SEG
                  c) extract data message: If monitoring data has more than one chunk, it will send subsequent
                  Interest messages.
                : Input argument
                   a) Name of SEG (e.g., SEG_1)
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
import argparse
import os
import random
import subprocess
import sys
import time
import traceback
from pyndn import Data
from pyndn import Face
from pyndn import Interest
from pyndn import InterestFilter
from pyndn import Name
from pyndn.security import KeyChain

from monitoringDB import InfluxDBWriter
from modules.tools import dockerctl
from modules.tools.enumerate_publisher import EnumeratePublisher


class MonitoringManager_Main(object):
    def __init__(self, name):
        self.outstanding = dict()
        self.isDone = False
        self.keyChain = KeyChain()
        self.face = Face("127.0.0.1")
        self.nameInput = name
        self.script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
        self.script_dir = os.path.split(self.script_path)[0] #i.e. /path/to/dir/

    def run(self):

        try:

            self._sendNextInterest(Name(self.nameInput))

            while not self.isDone:
                self.face.processEvents()
                time.sleep(0.01)

        except RuntimeError as e:
            print "ERROR: %s" %  e

        return True

    def _sendNextInterest(self, name):
        interest = Interest(name)
        uri = name.toUri()

        interest.setInterestLifetimeMilliseconds(12000)
        interest.setMustBeFresh(True)

        if uri not in self.outstanding:
            self.outstanding[uri] = 1
        self.face.expressInterest(interest, self._onData, self._onTimeout)
        print "Sent Interest for %s" % uri

    def _onData(self, interest, data):
        dataName = data.getName()
        data_name_components = dataName.toUri().split("/")
        if "monitoring" in data_name_components:
            #nodeName = 'SEG_1'
            nodeName = data_name_components[data_name_components.index("monitoring") + 1]
            #timeStamp = data_name_components[data_name_components.index("service_monitoring") + 2]
            #print 'Receive Data from %s' % nodeName
            #print 'Timestamp %s' % timeStamp
            rel_path = "Monitoring_DB"
            abs_path = os.path.join(self.script_dir, rel_path)
            print "path of monitoring Pi:%s" %abs_path
            f = os.popen('date +%s')
            #timestamp = f.read()
            fileName = 'status'+'-' + nodeName + '.json'
            print "Monitoring File name:%s" %fileName
            file_path = os.path.join(abs_path, fileName)
            if os.path.exists(file_path) == True:
                print 'remove old monitoring Data'
                os.remove(file_path)
            self._extractData_message(abs_path, fileName, data)
            self.Monitoring_Manager = InfluxDBWriter(abs_path, fileName)
            self.Monitoring_Manager.write()

        else:
            print "function is not yet ready"

        currentInterestName = interest.getName()
        # Delete the Interest name from outstanding INTEREST dict as reply DATA has been received.
        del self.outstanding[currentInterestName.toUri()]
        self.isDone = True


    def _onTimeout(self, interest):
        name = interest.getName()
        uri = name.toUri()

        print "TIMEOUT #%d: %s" % (self.outstanding[uri], uri)
        self.outstanding[uri] += 1

        if self.outstanding[uri] <= 3:
            self._sendNextInterest(name)
        else:
            self.isDone = True


    def onRegisterFailed(self, prefix):
        print "Register failed for prefix", prefix.toUri()
        self.isDone = True

    def _extractData_message(self, path, fileName, data):
        payload = data.getContent()
        dataName = data.getName()
        dataName_size = dataName.size()
        print "Extracting Data message name: ", dataName.toUri()
        #print "Received data: ", payload.toRawStr()
        if not os.path.exists(path):
                os.makedirs(path)

        with open(os.path.join(path, fileName), 'ab') as temp_file:
            temp_file.write(payload.toRawStr())
            # if recieved Data is a segment of the file, then need to fetch remaning segments
            # try if segment number is existed in Data Name
        try:
            dataSegmentNum = (dataName.get(dataName_size - 1)).toSegment()
            lastSegmentNum = (data.getMetaInfo().getFinalBlockId()).toNumber()
            print "dataSegmentNum" + str(dataSegmentNum)
            print "lastSegmentNum" + str(lastSegmentNum)

            # If segment number is available and what have recieved is not the FINAL_BLOCK, then fetch the NEXT segment
            if lastSegmentNum != dataSegmentNum:
                interestName = dataName.getSubName(0, dataName_size - 1)
                interestName = interestName.appendSegment(dataSegmentNum + 1)
                ### Fix this
                self._sendNextInterest(interestName)
            # If segment number is available and what have recieved is the FINAL_BLOCK, then EXECUTE the configuration script
            ### Recieve all chunks of data --> Execute it here
            if lastSegmentNum == dataSegmentNum:
                print "Received complete Data message: %s  " % fileName

        except RuntimeError as e:
            print "ERROR: %s" % e
            self.isDone = True

#if __name__ == '__main__':

    #nameInput  = raw_input('Enter Name of Content ')
    #try:

        #Consumer().run()

    #except:
        #traceback.print_exc(file=sys.stdout)
        #sys.exit(1)
