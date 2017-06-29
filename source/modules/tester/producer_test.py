from pprint import pprint
from modules.DataStore.dataStore import DataStore

from modules.Monitoring.monitoringAgent_thread import producerThread

DS = DataStore()
#print DS.table

######### Adding Prefix and content in DS
namePrefix1 = '/adisorn/file1'
type = 'file'
content = '/home/adisorn/test.txt'
DS.putDataStore(namePrefix1, type, content)
#print DS.table
print 'add content name: %s' %namePrefix1
print 'Content type: %s' %DS.getDataStore_Type(namePrefix1)
print 'Content: %s' %DS.getDataStore_Content(namePrefix1)

namePrefix2 = '/adisorn/file2'
type = 'text'
content = '/home/adisorn/test2.txt'
DS.putDataStore(namePrefix2, type, content)
#print DS.table
print 'add content name: %s' %namePrefix2
print 'Content type: %s' %DS.getDataStore_Type(namePrefix2)
print 'Content: %s' %DS.getDataStore_Content(namePrefix2)

namePrefix3 = '/picasso/monitoring/SEG_1'
type = 'function'
content = 'monitoring'
DS.putDataStore(namePrefix3, type, content)
#print DS.table
print 'add content name: %s' %namePrefix3
print 'Content type: %s' %DS.getDataStore_Type(namePrefix3)
print 'Content: %s' %DS.getDataStore_Content(namePrefix3)

DS.creaDataStore_json(DS.table)

# test = DS.readDataStore_json()
# pprint(test)
#
# print test[namePrefix2]['Content']
exitFlag = 0
print "Test Producer"
thread1 = producerThread(1, "Thread-1", 'SEG_1', namePrefix1, DS)
thread2 = producerThread(2, "Thread-2", 'SEG_1', namePrefix2, DS)
thread3 = producerThread(3, "Thread-3", 'SEG_1', namePrefix3, DS)

thread1.start()
thread2.start()
thread3.start()


print "Exiting Main Thread"


# try:
#     #thread.start_new_thread(producer1.run())
#     thread.start_new_thread(Producer, ('/ndn/test1'))
#     thread.start_new_thread(Producer, ('/ndn/test2'))
# except:
#     print "Error: unable to start thread"







