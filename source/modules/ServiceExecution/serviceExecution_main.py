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

import argparse
import os
import sys
import threading
import time
import traceback
from pprint import pprint
from pyndn import Data
from pyndn import Exclude
from pyndn import Face
from pyndn import Interest
from pyndn import InterestFilter
from pyndn import Name
from pyndn.security import KeyChain

import modules.tools.dockerctl
from modules.tools import ndnMessage_Helper, dockerctl
from modules.tools.enumerate_publisher import EnumeratePublisher
from modules.tools.termopi import termopi # class with dictionary data structure
import string

class Service_Execution_Main(object):
    def __init__(self, producerName, namePrefix):
        self.configPrefix = Name(namePrefix)
        prefix_pullService = "/picasso/pull_Service/"
        self.prefix_pullService = Name(prefix_pullService)
        self.Datamessage_size = 2000000 #20MB --> Max Size from modified NDN
        self.window = 1
        self.producerName = producerName
        self.outstanding = dict()
        self.isDone = False
        self.keyChain = KeyChain()
        self.face = Face("127.0.0.1")
        self.script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
        self.script_dir = os.path.split(self.script_path)[0] #i.e. /path/to/dir/
        self.interestLifetime = 12000000
        self.num_deployedContainer = 0
        self.lastChunk_window = 0
        self.lastChunk_sent = 0

        folder_name = "SEG_repository/"
        self.repo_path = os.path.join(self.script_dir, folder_name)
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)

        folder_name = "Migration_cost/"
        self.timestamp_path = os.path.join(self.script_dir, folder_name)
        if not os.path.exists(self.timestamp_path):
            os.makedirs(self.timestamp_path)


    def run(self):
        try:
            self.face.setCommandSigningInfo(self.keyChain, self.keyChain.getDefaultCertificateName())
            self.face.registerPrefix(self.configPrefix, self.onInterest_pushService, self.onRegisterFailed)
            print "Registered prefix : " + self.configPrefix.toUri()

            self.face.setCommandSigningInfo(self.keyChain, self.keyChain.getDefaultCertificateName())
            self.face.registerPrefix(self.prefix_pullService, self.onInterest_pullService, self.onRegisterFailed)
            print "Registered prefix : " + self.prefix_pullService.toUri()

            while not self.isDone:
                self.face.processEvents()
                time.sleep(0.01)

        except RuntimeError as e:
            print "ERROR: %s" %  e

    def onInterest_pushService(self, prefix, interest, face, interestFilterId, filter):
        interestName = interest.getName()
        ### Delete image_file in SEG_Repe. This is just for migration cost experiment.
        delete_service_command = 'rm ' + self.repo_path + '*'
        os.system(delete_service_command)

        print "Interest Name: %s" %interestName
        interest_name_components = interestName.toUri().split("/")
        if "service_deployment_push" in interest_name_components:
            image_fileName = interest_name_components[interest_name_components.index("service_deployment_push") + 2]
            print 'Deploy service: %s' %image_fileName
            print 'Start service deployment'

            if dockerctl.has_ServiceInfo(image_fileName) == True:
                print 'Has description for service deployment'
                ExecutionType = dockerctl.get_ExecutionType(image_fileName)
                if ExecutionType == 'singleWebContainer':
                    print 'Deployment uses dockerctl'
                    deployment_status = dockerctl.deployContainer(image_fileName, self.num_deployedContainer)
                    if  deployment_status == 'pull_image':
                        print 'Service: %s is not locally cached, pull from Repo' % image_fileName
                        prefix_pullImage = Name("/picasso/service_deployment_pull/" + image_fileName)
                        print 'Sending Interest message: %s' % prefix_pullImage
                        self._sendNextInterest(prefix_pullImage, self.interestLifetime, 'pull')
                        filename = image_fileName + '.txt'
                        self.StartTimeStamp_MigrationTime(filename)

                    elif deployment_status == 'done':
                        print 'Service:%s is successfully deployed' %image_fileName
                        self.num_deployedContainer += 1
                    elif deployment_status == 'error':
                        print 'Error in deployment process'
                    else:
                        print 'Code bug'

                elif ExecutionType == 'DockerCompose':
                    print 'Deployment uses docker compose'
                    if dockerctl.has_imagefile(image_fileName) == True:
                        print 'Load image and run service'
                        dockerctl.run_DockerCompose_source(image_fileName)
                    else:
                        print 'Service: %s is not locally cached, pull from Repo' % image_fileName
                        prefix_pullImage = Name("/picasso/service_deployment_pull/" + image_fileName)
                        print 'Sending Interest message: %s' % prefix_pullImage
                        self._sendNextInterest(prefix_pullImage, self.interestLifetime, 'pull')
                        timestamp_file = image_fileName + '.txt'
                        self.StartTimeStamp_MigrationTime(timestamp_file)
                else:
                    print 'Execution method is not yet implemented'

            else:
                print 'Deployment description is not available'
        else:
            print "Interest name mismatch"

    def onInterest_pullService(self, prefix, interest, face, interestFilterId, filter):
        ### This function is used in ACM ICN where the SEG receive the trigger message to pull the service
        interestName = interest.getName()
        print "Interest Name: %s" %interestName
        interest_name_components = interestName.toUri().split("/")
        image_fileName = interest_name_components[interest_name_components.index("pull_Service") + 1]
        if "pull_Service" in interest_name_components:
            prefix_pullImage = Name("/picasso/service_deployment_pull/" + image_fileName)
            print 'Sending Interest message: %s' % prefix_pullImage
            self._sendNextInterest(prefix_pullImage, self.interestLifetime, 'pull')

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

        if "service_deployment_pull" in data_name_components:
            fileName = data_name_components[data_name_components.index("service_deployment_pull") + 1]
            rel_path = "SEG_repository"
            abs_path = os.path.join(self.script_dir, rel_path)
            print "path of SEG_repository:%s" %abs_path
            print "Service File name:%s" %fileName
            file_path = os.path.join(abs_path, fileName)
            dataSegmentNum = (dataName.get(dataName_size - 1)).toSegment()
            lastSegmentNum = (data.getMetaInfo().getFinalBlockId()).toNumber()
            print "dataSegmentNum" + str(dataSegmentNum)
            print "lastSegmentNum" + str(lastSegmentNum)
            if dataSegmentNum == 0:
                print 'Start counting received chunks'
                self.StartCountingReceivedChunks(dataSegmentNum, lastSegmentNum+1)
            else:
                self.UpdatingReceivedChunks(dataSegmentNum)

            if self.request_SubsequenceDataChunk(abs_path, fileName, data, self.window) == True:
                timestamp_file = fileName + '.txt'
                self.StopTimeStamp_MigrationTime(timestamp_file )
                print 'Load image and run service'
                if dockerctl.has_ServiceInfo(fileName) == True:
                    print 'Has description for service deployment'
                    ExecutionType = dockerctl.get_ExecutionType(fileName)
                    if ExecutionType == 'singleWebContainer':
                        print 'Deployment uses dockerctl'
                        if dockerctl.deployContainer(fileName, self.num_deployedContainer) == 'error':
                            print 'Image:%s cannot be deployed' %fileName
                    elif ExecutionType == 'DockerCompose':
                        dockerctl.run_DockerCompose_source(fileName)
                    else:
                        print 'Execution method is not yet implemented'


        else:
             print "function is not yet ready"

        currentInterestName = interest.getName()
        # Delete the Interest name from outstanding INTEREST dict as reply DATA has been received.
        del self.outstanding[currentInterestName.toUri()]
        #self.isDone = True


    def _onTimeout(self, interest):
        name = interest.getName()
        uri = name.toUri()

        print "TIMEOUT #%d: %s" % (self.outstanding[uri], uri)
        self.outstanding[uri] += 1

        if self.outstanding[uri] <= 3:
            self._sendNextInterest(name, self.interestLifetime, 'pull')
        else:
            #self.isDone = True
            print 'Cannot pull content for Interest: %s' %name

    def request_SubsequenceDataChunk(self, path, fileName, data, window):
        payload = data.getContent()
        dataName = data.getName()
        dataName_size = dataName.size()
        timestamp_file = fileName + '.txt'
        self.StartExtraction_TimeStamp(timestamp_file)
        print "Extracting Data message name: ", dataName.toUri()
        if not os.path.exists(path):
                os.makedirs(path)

        with open(os.path.join(path, fileName), 'ab') as temp_file:
            temp_file.write(payload.toRawStr())
        try:
            dataSegmentNum = (dataName.get(dataName_size - 1)).toSegment()
            lastSegmentNum = (data.getMetaInfo().getFinalBlockId()).toNumber()
            self.FinishExtraction_TimeStamp(timestamp_file)

            if dataSegmentNum == self.lastChunk_window:
                print 'Send Interest of next window frame'
                firstChunk_sent = self.lastChunk_window + 1
                self.lastChunk_window = self.lastChunk_window + window
                if self.lastChunk_window <= lastSegmentNum:
                    print 'This is NOT the last frame'
                    self.lastChunk_sent = self.lastChunk_window
                else:
                    print 'This is the last frame'
                    self.lastChunk_sent = lastSegmentNum
                for chunkID in range (firstChunk_sent, self.lastChunk_sent + 1):
                    interestName = dataName.getSubName(0, dataName_size - 1)
                    interestName = interestName.appendSegment(chunkID)
                    self._sendNextInterest(interestName, self.interestLifetime, 'pull')


            else:
                print 'Already sent window frame, Waiting for Data message'

            if lastSegmentNum == dataSegmentNum:
                print 'Received last chunk of content'
                print 'Stop Sending Interest'
                self.lastChunk_window = 0
                self.lastChunk_sent = 0

            TotalReceivedChunk = sum(list(self.receivedContentChunk))
            if TotalReceivedChunk == lastSegmentNum+1:
                print "Received complete image: %s, EXECUTED !!!!" % fileName
                return True

        except RuntimeError as e:
                print "ERROR: %s" % e
                self.isDone = True

    def StartCountingReceivedChunks(self, chunkID, TotalNumChunks):
        self.receivedContentChunk = [0 for i in range(TotalNumChunks)]
        self.receivedContentChunk[chunkID] = 1
        print self.receivedContentChunk
    def UpdatingReceivedChunks(self, chunkID):
        self.receivedContentChunk[chunkID] = 1
        print self.receivedContentChunk

    def StartTimeStamp_MigrationTime (self, filename):
        outputfile_path = os.path.join(self.timestamp_path,filename)
        if os.path.exists(outputfile_path) == True:
            print 'timestamp file is already existed'
        else:
            print 'create output file'
            open(outputfile_path, 'a').close()

        file = open(outputfile_path, 'a')
        #file.write('Start Migration:  ' + time.strftime("%a, %d %b %Y %X +0000", time.gmtime()) + '\n')
        file.write('Service Migration Start:  ' + time.ctime() + '\n')
        file.write('Start:  ' + str(time.time()) + '\n')
        file.close()

    def StartExtraction_TimeStamp(self, filename):
        outputfile_path = os.path.join(self.timestamp_path, filename)
        file = open(outputfile_path, 'a')
        file.write('Extracting_Start: ' + str(time.time()) + '\n')
        file.close()

    def FinishExtraction_TimeStamp(self, filename):
        outputfile_path = os.path.join(self.timestamp_path, filename)
        file = open(outputfile_path, 'a')
        file.write('Extracting_End: ' + str(time.time()) + '\n')
        file.close()

    def StopTimeStamp_MigrationTime (self, filename):
        outputfile_path = os.path.join(self.timestamp_path, filename)
        file = open(outputfile_path, 'a')
        file.write('Service Migration Finish:  ' + time.ctime() + '\n')
        file.write('Finish: ' + str(time.time()) + '\n')
        file.close()