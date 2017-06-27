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


# from NOMAD import enumerate_publisher
class trigger(object):
    def __init__(self):

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

        prefix_DE = "/picasso/service_deployment/SEG_1"
        self.prefix_DE = Name(prefix_DE)

        # Default configuration of NDN
        self.outstanding = dict()
        self.isDone = False
        self.keyChain = KeyChain()
        self.face = Face("127.0.0.1")

        self.face.setCommandSigningInfo(self.keyChain, \
                                        self.keyChain.getDefaultCertificateName())

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
            # while not self.isDone:
            #
            #     self.face.processEvents()
            #     time.sleep(0.01)

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
if __name__ == '__main__':

    try:

        trigger().run()

    except:
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)



