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
import os
import time
from de import de
import migrationfunc
from pyndn import Data
from pyndn import Face
from pyndn import Interest
from pyndn import InterestFilter
from pyndn import Name
from pyndn.security import KeyChain

from modules.tools import dockerctl
from modules.tools.enumerate_publisher import EnumeratePublisher


class Decision_Engine_Main(object):
    def __init__(self, namePrefix):
        self.outstanding = dict()
        self.isDone = False
        self.keyChain = KeyChain()
        self.face = Face("127.0.0.1")
        self.configPrefix = Name(namePrefix)
        self.script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
        self.script_dir = os.path.split(self.script_path)[0] #i.e. /path/to/dir/
        self.interestLifetime = 12000
        folder_name = "SC_repository/"
        rel_path = os.path.join(self.script_dir, folder_name)
        prefix_startDE = "/picasso/start_de/"
        self.prefix_startDE = Name(prefix_startDE)
        self.prefix_deployService = '/picasso/service_deployment_push/'
        self.json_server_Spec_default= { # This is only an skeleton
                                    'par':{ #  service parameters
                                    'serviceName':  'nameOfService',
                                    'imageName':    'NameOfImageToIstantiateService',
                                    'imageSize':    'sizeOfImage',
                                    'maxConReq':    'maxNumConcurrentRequestsThatAnIntanceCanHandle',
                                    'startUpTime':  'timeToInstatiateService'
                                    },
                                    'QoS':{ #QoS parameters expected from the service
                                    'responseTime':  'resposeTimeExpectedFromService',
                                    'availability': 'availabilityExpectedFromService',
                                    'numConReq':     'numConcurrentRequestsToBeHandledByService'
                                    }
                                  }



        if not os.path.exists(rel_path):
            os.makedirs(rel_path)

    def run(self):

        try:

            ### This face is used to send an image to the SEG
            self.face.setCommandSigningInfo(self.keyChain, self.keyChain.getDefaultCertificateName())
            self.face.registerPrefix(self.configPrefix, self.onInterest_PullService, self.onRegisterFailed)

            #### This face is used to start the algorithm of decision engine. The Interest is sent by trigger module
            #### This face is for testing propose
            self.face.setCommandSigningInfo(self.keyChain, self.keyChain.getDefaultCertificateName())
            self.face.registerPrefix(self.prefix_startDE, self.onInterest_StartDE, self.onRegisterFailed)

            print "Registered prefix : " + self.configPrefix.toUri()

            while not self.isDone:
                self.face.processEvents()
                time.sleep(0.01)

        except RuntimeError as e:
            print "ERROR: %s" %  e

        return True

    def onInterest_StartDE(self, prefix, interest, face, interestFilterId, filter):
        interestName = interest.getName()
        print "Interest Name: %s" %interestName
        interest_name_components = interestName.toUri().split("/")
        if "start_de" in interest_name_components:
            #print 'Query database'
            print 'Call decision engine algorithm'
            parent_dir = os.path.split(self.script_dir)[0]
            monitor_path = os.path.join(self.script_dir, parent_dir, 'Monitoring', 'Monitoring_DB')
            print monitor_path
            myDE = de(monitor_path)
            json_lst_dict = myDE.get_lst_of_dictionaries()
            json_server_Spec = self.json_server_Spec_default
            node_name = myDE.selectHost_to_deploy_firstInstance(json_lst_dict, json_server_Spec)
            print 'Selected Host Name %s' %node_name
            ### User will add this parameter via trigger
            service_name = 'uhttpd.tar'
            print 'Start service deployment'
            deployService = self.prefix_deployService + node_name + '/' + service_name
            config_prefix_deployService = Name(deployService)
            interest = Interest(config_prefix_deployService)
            interest.setInterestLifetimeMilliseconds(self.interestLifetime)
            interest.setMustBeFresh(True)
            self.face.expressInterest(interest, None, None)  ## set None --> sent out only, don't wait for Data and Timeout
            print "Sent Push Interest to SEG %s" % config_prefix_deployService
        else:
            print "Interest name mismatch"

    def onInterest_PullService(self, prefix, interest, face, interestFilterId, filter):
        interestName = interest.getName()
        data = Data(interestName)
        print "Interest Name: %s" %interestName
        interest_name_components = interestName.toUri().split("/")
        if "service_deployment_pull" in interest_name_components:
            ## Extract filename from Interest name
            filename = "uhttpd.tar"
            folder_name = "SC_repository/"
            rel_path = os.path.join(self.script_dir, folder_name)
            if not os.path.exists(rel_path):
                os.makedirs(rel_path)
            abs_file_path = os.path.join(rel_path, filename)
            freshness = 10000 #milli second, content will be deleted from the cache after freshness period
            self.sendingFile(abs_file_path, interest, face, freshness)
        else:
            print "Interest name mismatch"

    def onRegisterFailed(self, prefix):
        print "Register failed for prefix", prefix.toUri()
        self.isDone = True

    def sendingFile(self, file_path, interest, face, freshness):
        print "Sending File Function"
        interestName = interest.getName()
        interestNameSize = interestName.size()

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

        except ValueError as err:
            print "ERROR: %s" % err
