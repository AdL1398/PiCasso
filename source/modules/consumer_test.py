from consumer import Consumer
from consumerThread import consumerThread
#import threading
from threading import Timer, Thread, Event
import os
import time

print "Test Consumer"
f = os.popen('date +%s')
timestamp = f.read()
print 'Timestamp %s' % timestamp
namePrefix1 = '/picasso/monitoring/SEG_1/'
namePrefix2 = '/picasso/monitoring/SEG_2/'

#thread1 = consumerThread(1, "Thread-1", 1, namePrefix1)
#thread2 = consumerThread(2, "Thread-2", 2, namePrefix2)

stopFlag = Event()
thread1 = consumerThread(1, "Thread-1", 1, namePrefix1, stopFlag)
thread2 = consumerThread(2, "Thread-2", 2, namePrefix2, stopFlag)

#thread = MyThread(stopFlag)
thread1.start()
thread2.start()
# this will stop the timer
#stopFlag.set()

#thread1.start()
#thread1.start()
#thread2.start()


