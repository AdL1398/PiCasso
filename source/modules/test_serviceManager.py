from consumer import Consumer
from consumerThread import consumerThread
#import threading
from threading import Timer, Thread, Event
import sys
import traceback
import os
import time

class ServiceManaer(object):
    def __init__(self):
        self.namePrefix1 = '/picasso/monitoring/SEG_1/'
        self.namePrefix2 = '/picasso/monitoring/SEG_2/'

    def run(self):
        try:
            #instantiate DB here
            #instantiate Grafana
            # Create Thread
            stopFlag = Event()
            thread1 = consumerThread(1, "Thread-1", 1, self.namePrefix1, stopFlag)
            thread1.start()

        except RuntimeError as e:
            print "ERROR: %s" %  e

        return True

if __name__ == '__main__':

    #nameInput  = raw_input('Enter Name of Content ')
    print 'Start Service Manager'
    try:
        ServiceManaer().run()
    except:
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)
