import sys
import time
import argparse
import traceback
import os
import subprocess


from pyndn import Interest
from pyndn import Data
from pyndn import Exclude
from pyndn import Name
from pyndn import Face
from pyndn import InterestFilter
from pyndn.security import KeyChain
from modules.tools.enumerate_publisher import EnumeratePublisher

# from NOMAD import enumerate_publisher
class trigger(object):
    def __init__(self):

        self.script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
        self.script_dir = os.path.split(self.script_path)[0] #i.e. /path/to/dir/
        self.Datamessage_size = 8000 #8kB --> Max Size from NDN standard

        prefix_serviceDiscovery = "/sm/service_discovery"
        self.prefix_serviceDiscovery = Name(prefix_serviceDiscovery)

        prefix_serviceRegistration = "/sm/service_registration"
        self.prefix_serviceRegistration = Name(prefix_serviceRegistration)

        prefix_serviceMigration = "/sm/service_migration"
        self.prefix_serviceMigration = Name(prefix_serviceMigration)

        prefix_serviceMigrationPush = "/sm/service_migration/push"
        self.prefix_serviceMigrationPush = Name(prefix_serviceMigrationPush)

        prefix_trigger = "/trigger"
        self.prefix_trigger = Name(prefix_trigger)

        prefix_start_DTN_demo = "/sm/start_DTN_demo"
        self.prefix_start_DTN_demo = Name(prefix_start_DTN_demo)

        prefix_serviceMigration_KEBAPP = "/kebapp/maps/routefinder/"
        self.prefix_serviceMigration_KEBAPP = Name(prefix_serviceMigration_KEBAPP)

        prefix_DE = "/picasso/service_deployment_push/SEG_1/uhttpd.tar/"
        self.prefix_DE = Name(prefix_DE)

        prefix_deployment_pull = "/picasso/service_deployment_pull/"
        self.prefix_deployment_pull = Name(prefix_deployment_pull)

        # Default configuration of NDN
        self.outstanding = dict()
        self.isDone = False
        self.keyChain = KeyChain()
        self.face = Face("127.0.0.1")

        self.face.setCommandSigningInfo(self.keyChain, \
                                        self.keyChain.getDefaultCertificateName())
        self.face.registerPrefix(self.prefix_deployment_pull, self.onInterest_PullService, self.onRegisterFailed)
        print "Registering prefix : " + self.prefix_deployment_pull.toUri()

    def run(self):
        try:
            # send Interest message to retrieve data
            #self.sendNextInterest(self.prefix_serviceMigration)
            demo_name = raw_input('Enter name of the Demo (DTN or KEBAPP or DE) ')
            if demo_name == 'DTN':
                print 'Start SM-DTN Demo'
                name_prefix = self.prefix_start_DTN_demo
            if demo_name == 'KEBAPP':
                print 'Start SM-KEBAPP demo'
                name_prefix = self.prefix_serviceMigration_KEBAPP
            if demo_name == 'DE':
                print 'Start DE test'
                name_prefix = self.prefix_DE
            else:
                print 'Try Again'
            self.sendPushInterest(name_prefix)

            while not self.isDone:
                self.face.processEvents()
                time.sleep(0.01)

        except RuntimeError as e:
            print "ERROR: %s" % e

    def sendPushInterest(self, name):
        interest = Interest(name)
        uri = name.toUri()

        interest.setInterestLifetimeMilliseconds(4000)
        interest.setMustBeFresh(True)

        if uri not in self.outstanding:
            self.outstanding[uri] = 1

        # self.face.expressInterest(interest, self.onData, self._onTimeout)
        self.face.expressInterest(interest, None, None)  ## set None --> sent out only, don't wait for Data and Timeout
        print "Sent Push-Interest for %s" % uri

    def onTimeout(self, interest):
        name = interest.getName()
        uri = name.toUri()

        print "TIMEOUT #%d: %s" % (self.outstanding[uri], uri)
        self.outstanding[uri] += 1

        if self.outstanding[uri] <= 3:
            self.sendNextInterest(name)
        else:
            self.isDone = True

    def onInterest_PullService(self, prefix, interest, face, interestFilterId, filter):
        interestName = interest.getName()
        data = Data(interestName)
        print "Interest Name: %s" %interestName
        interest_name_components = interestName.toUri().split("/")
        if "service_deployment_pull" in interest_name_components:
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


if __name__ == '__main__':

    try:

        trigger().run()

    except:
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)



