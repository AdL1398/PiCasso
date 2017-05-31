from producer import Producer
import threading

class producerThread (threading.Thread):
   def __init__(self, threadID, threadName, producerName, namePrefix, DS):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.threadname = threadName
      self.producerName = producerName
      self.namePrefix = namePrefix
      self.DS = DS

   def run(self):
      print "Starting " + self.threadname
      producer = Producer(self.namePrefix, self.DS, self.producerName)
      producer.run()
      print "Exiting " + self.threadname

