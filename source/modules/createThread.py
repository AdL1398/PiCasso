from producer import Producer
import threading
import time

class createThread (threading.Thread):
   def __init__(self, threadID, name, counter, namePrefix):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      self.namePrefix = namePrefix
   def run(self):
      print "Starting " + self.name
      producer = Producer(self.namePrefix)
      producer.run()
      print "Exiting " + self.name
