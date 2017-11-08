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

        self.prefix_DE = "/picasso/start_de/"
        # Default configuration of NDN
        self.outstanding = dict()
        self.isDone = False
        self.keyChain = KeyChain()
        self.face = Face("127.0.0.1")

        self.face.setCommandSigningInfo(self.keyChain, \
                                        self.keyChain.getDefaultCertificateName())
        #self.face.registerPrefix(self.prefix_deployment_pull, self.onInterest_PullService, self.onRegisterFailed)
        #print "Registering prefix : " + self.prefix_deployment_pull.toUri()

    def run(self):
        try:
            # send Interest message to retrieve data
            #self.sendNextInterest(self.prefix_serviceMigration)
            print 'Available services'
            print '   (1) cloudsuite_webserver_PI.tar  --- 495   MB'
            print '   (2) cloudsuite_db_server_PI.tar  --- 430   MB'
            print '   (3) cloudsuite_memcached_PI.tar  --- 366   MB'
            print '   (4) armbuild_debian.tar          --- 145   MB'
            print '   (5) alpine_armhf_nginx.tar       --- 14.95 MB'
            print '   (6) armhf_alpine.tar             --- 3.85  MB'
            print '   (7) rpi_busybox_httpd.tar        --- 2.2   MB'
            print '   (8) rpi_nano_httpd.tar           --- 110   kB'

            input_service = raw_input('Choose service to be deployed (type number, e.g., 1): ')
            input_node = raw_input('Select node to migrate service (e.g., SEG_1): ')

            if input_service == '1':
                print 'Start deploy cloudsuite web server'
                service_name = 'cloudsuite_webserver_PI.tar'

            elif input_service == '2':
                print 'Start deploy cloudsuite db server'
                service_name = 'cloudsuite_db_server_PI.tar'

            elif input_service == '3':
                print 'Start deploy Start deploy cloudsuite memcached server'
                service_name = 'cloudsuite_memcached_PI.tar'

            elif input_service == '4':
                print 'Start deploy debian'
                service_name = 'armbuild_debian.tar'

            elif input_service == '5':
                print 'Start deploy nginx'
                service_name = 'alpine_armhf_nginx.tar'

            elif input_service == '6':
                print 'Start deploy alpine linux'
                service_name = 'armhf_alpine.tar'

            elif input_service == '7':
                print 'Start deploy busybox-httpd'
                service_name = 'rpi_busybox_httpd.tar'

            elif input_service == '8':
                print 'Start deploy nano-httpd'
                service_name = 'rpi_nano_httpd.tar'

            else:
                print 'Chosen service is not available'

            name_prefix = self.prefix_DE + service_name + '/' + input_node
            print 'name prefix: %s' % name_prefix
            self.sendInterest_to_DE(Name(name_prefix))

        except RuntimeError as e:
            print "ERROR: %s" % e

    def sendInterest_to_DE(self, name):
        interest = Interest(name)
        interestName = interest.getName()

        interest.setInterestLifetimeMilliseconds(4000)
        interest.setMustBeFresh(True)

        #if uri not in self.outstanding:
            #self.outstanding[uri] = 1

        # self.face.expressInterest(interest, self.onData, self._onTimeout)
        self.face.expressInterest(interest, None, None)  ## set None --> sent out only, don't wait for Data and Timeout
        print "Sent Push-Interest for %s" % interestName

if __name__ == '__main__':

    try:

        trigger().run()

    except:
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)



