from monitoringAgent import Monitoring_Agent
import threading

class MonitoringAgent_Thread (threading.Thread):
   def __init__(self, threadID, threadName, producerName, namePrefix, DS):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.threadname = threadName
      self.producerName = producerName
      self.namePrefix = namePrefix
      self.DS = DS

   def run(self):
      print "Starting " + self.threadname
      monitoring_agent = Monitoring_Agent(self.namePrefix, self.DS, self.producerName)
      monitoring_agent.run()
      print "Exiting " + self.threadname

