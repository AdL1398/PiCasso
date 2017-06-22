#from consumer import Consumer
#from consumerThread import consumerThread
from monitoringThread import MonitoringThread
from threading import Timer, Thread, Event
import sys
import traceback
import os
import time

class ServiceManaer(object):
    def __init__(self):
        self.namePrefix1 = '/picasso/monitoring/SEG_1/'
        self.namePrefix2 = '/picasso/monitoring/SEG_2/'
        self.monitoring_frequency = 10

    def run(self):
        try:
            #instantiate DB here
            #instantiate Grafana
            # Create Thread
            stopFlag = Event()
            print 'Start Monitoring Manager'
            thread1 = MonitoringThread(1, "Thread-1", 1, self.namePrefix1, stopFlag, self.monitoring_frequency)
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
