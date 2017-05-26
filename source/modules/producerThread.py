from producer import Producer
import threading

class producerThread (threading.Thread):
   def __init__(self, threadID, name, counter, namePrefix, DS):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      self.namePrefix = namePrefix
      self.DS = DS

   def run(self):
      print "Starting " + self.name
      producer = Producer(self.namePrefix, self.DS)
      producer.run()
      print "Exiting " + self.name

