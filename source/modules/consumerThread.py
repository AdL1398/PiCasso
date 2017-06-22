from consumer import Consumer
import threading
import time

class consumerThread (threading.Thread):
   def __init__(self, threadID, name, counter, namePrefix, event):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      self.namePrefix = namePrefix
      self.stopped = event

   def run(self):
      print "Starting " + self.name
      stopFlag = False
      while not self.stopped.wait(10):
         print "creating thread for: %s" %self.namePrefix
         # call a function
         consumer = Consumer(self.namePrefix)
         consumer.run()
      print "Exiting " + self.name
