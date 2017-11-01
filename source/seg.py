import sys
import os
import traceback
from pprint import pprint
from modules.DataStore.dataStore import DataStore
from modules.ServiceExecution.serviceExecution_thread import Service_Execution
from modules.Monitoring.monitoringAgent_thread import Monitoring_Agent


class SEG(object):
    def __init__(self, node_id):
        #self.DS = DataStore()
        self.script_path = os.path.abspath(__file__)  # i.e. /path/to/dir/foobar.py
        self.script_dir = os.path.split(self.script_path)[0]  # i.e. /path/to/dir/
        self.seg_ID = node_id
        self.namePrefix_Monitor = '/picasso/monitoring/' + self.seg_ID
        self.namePrefix_SE = '/picasso/service_deployment_push/' + self.seg_ID


    def run(self):
        try:
            exitFlag = 0
            os.system("docker rm -f $(docker ps -a -q)")
            print "Start %s" %self.seg_ID
            monitoring_agent = Monitoring_Agent(1, "Thread-Monitoring", self.seg_ID, self.namePrefix_Monitor)
            monitoring_agent.start()

            serviceExecution_agent = Service_Execution(1, "Thread-SE", self.seg_ID, self.namePrefix_SE)
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
