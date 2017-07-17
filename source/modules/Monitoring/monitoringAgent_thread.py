from monitoringAgent import Monitoring_Agent_Main
import threading

class Monitoring_Agent(threading.Thread):
   def __init__(self, threadID, threadName, producerName, namePrefix):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.threadname = threadName
      self.producerName = producerName
      self.namePrefix = namePrefix
      #self.DS = DS

   def run(self):
      print "Starting " + self.threadname
      monitoring_agent = Monitoring_Agent_Main(self.namePrefix, self.producerName)
      monitoring_agent.run()
      print "Exiting " + self.threadname

