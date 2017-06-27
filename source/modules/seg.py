import sys
import traceback
from monitoringAgent_thread import MonitoringAgent_Thread
from serviceExecution_thread import ServiceExecution_Thread
from dataStore import DataStore
from pprint import pprint

class SEG(object):
    def __init__(self, node_id):
        #self.DS = DataStore()
        self.seg_ID = node_id
        self.namePrefix_Monitor = '/picasso/monitoring/' + self.seg_ID
        self.namePrefix_SE = '/picasso/service_deployment/' + self.seg_ID
        #type = 'function'
        #content = 'monitoring'
        #self.DS.putDataStore(self.namePrefix1, type, content)
        #print DS.table
        #print 'add content name: %s' %self.namePrefix1
        #print 'Content type: %s' %self.DS.getDataStore_Type(self.namePrefix1)
        #print 'Content: %s' %self.DS.getDataStore_Content(self.namePrefix1)
        #self.DS.creaDataStore_json(self.DS.table)

    def run(self):
        try:
            exitFlag = 0
            print "Start %s" %self.seg_ID
            monitoring_agent = MonitoringAgent_Thread(1, "Thread-Monitoring", self.seg_ID, self.namePrefix_Monitor)
            monitoring_agent.start()

            serviceExecution_agent = ServiceExecution_Thread(1, "Thread-SE", self.seg_ID, self.namePrefix_SE, )
            serviceExecution_agent.start()

            #print "Exiting Main Thread"

        except RuntimeError as e:
            print "ERROR: %s" % e

if __name__ == '__main__':

    node_id = raw_input('Enter SEG-ID (e.g., SEG_1) ')
    try:
        SEG(node_id).run()

    except:
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)
