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
        self.Datamessage_size = 8000 #8kB --> Max Size from NDN standard
        self.producerName = producerName
        self.outstanding = dict()
        self.isDone = False
        self.keyChain = KeyChain()
        self.face = Face("127.0.0.1")
        self.script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
        self.script_dir = os.path.split(self.script_path)[0] #i.e. /path/to/dir/
        self.interestLifetime = 12000
        folder_name = "SEG_repository/"
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

    def onInterest(self, prefix, interest, face, interestFilterId, filter):
        interestName = interest.getName()
        print "Interest Name: %s" %interestName
        interest_name_components = interestName.toUri().split("/")
        if "service_deployment" in interest_name_components:
            serviceName = interest_name_components[interest_name_components.index("service_deployment") + 2]
            print 'Deploy service: %s' %serviceName
            print 'Start service deployment'
            ## check image is running or not
            #Ger info from serviceInfo
            #serviceName = 'web-uhttpd'
            if dockerctl.deployContainer(serviceName) == False:
                print 'Service: %s is not locally cached, pull from Repo' % serviceName
                prefix_pullService = Name("/picasso/service_deployment/pull/" + serviceName)
                print 'Sending Interest message: %s' % prefix.pullService
                self._sendNextInterest(prefix.requestService, self.interestLifetime , 'pull')
        else:
            print "Interest name mismatch"

    def onRegisterFailed(self, prefix):
        print "Register failed for prefix", prefix.toUri()
        self.isDone = True

    def _sendNextInterest(self, name, lifetime, mode):
        interest = Interest(name)
        uri = name.toUri()

        interest.setInterestLifetimeMilliseconds(lifetime)
        interest.setMustBeFresh(True)

        if uri not in self.outstanding:
            self.outstanding[uri] = 1

        if mode == 'pull':
            print "Sent Pull Interest for %s" % uri
            self.face.expressInterest(interest, self._onData, self._onTimeout)
        elif mode == 'push':
            self.face.expressInterest(interest, None, None)  ## set None --> sent out only, don't wait for Data and Timeout
            print "Sent Push Interest for %s" % uri
        else:
            print "send Interest mode mismatch"

    def _onData(self, interest, data):
        payload = data.getContent()
        dataName = data.getName()
        dataName_size = dataName.size()
        print "Received data name: ", dataName.toUri()
        data_name_components = dataName.toUri().split("/")
        ## /picasso/service_deployment/pull/servicename/%%01
        if "service_deployment" in data_name_components:
            #nodeName = 'SEG_1'
            serviceName = data_name_components[data_name_components.index("service_deployment") + 2]
            fileName = dockerctl.serviceInfo[serviceName]['image_filename']
            rel_path = "SEG_repository"
            abs_path = os.path.join(self.script_dir, rel_path)
            print "path of SEG_repository:%s" %abs_path
            print "Service File name:%s" %fileName
            file_path = os.path.join(abs_path,fileName)
            self._extractData_message(abs_path, fileName, data)
            #self.Monitoring_Manager = InfluxDBWriter(abs_path, fileName)
            #self.Monitoring_Manager.write()
        else:
            print "function is not yet ready"

        currentInterestName = interest.getName()
        # Delete the Interest name from outstanding INTEREST dict as reply DATA has been received.
        del self.outstanding[currentInterestName.toUri()]
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
                self._sendNextInterest(interestName, self.interestLifetime, 'pull')
            # If segment number is available and what have recieved is the FINAL_BLOCK, then EXECUTE the configuration script
            ### Recieve all chunks of data --> Execute it here
            if lastSegmentNum == dataSegmentNum:
                print "Received complete Data message: %s  " % fileName

                docker_image_name = self.serviceInfo[fileName]['image_name']
                docker_port_host = self.serviceInfo[fileName]['port_host']
                docker_port_container = self.serviceInfo[fileName]['port_container']

                dockerctl.load_image(docker_image_name, self.path)
                if dockerctl.run_image(docker_image_name, docker_port_host, docker_port_container) == True:
                    print 'Running docker image %s ...' % docker_image_name
                else:
                    print 'Error: Cannot run image %s' % docker_image_name
                    #forward_request(webserver, port, s, data)
                    self.isDone = True

        except RuntimeError as e:
            print "ERROR: %s" % e
            self.isDone = True

