from consumer import Consumer
import threading
import time

class consumerThread (threading.Thread):
   def __init__(self, threadID, name, counter, namePrefix):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      self.namePrefix = namePrefix
   def run(self):
      print "Starting " + self.name
      consumer = Consumer(self.namePrefix)
      Consumer.run()
      print "Exiting " + self.name
