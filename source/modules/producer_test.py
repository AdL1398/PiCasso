from producerThread import producerThread
from dataStore import DataStore
from pprint import pprint

DS = DataStore()
#print DS.table

######### Adding Prefix and content in DS
namePrefix1 = '/adisorn/file1'
type = 'File'
filename = '/home/adisorn/test.txt'
DS.putDataStore(namePrefix1, type, filename)
#print DS.table
print 'add content name: %s' %namePrefix1
print 'Content type: %s' %DS.getDataStore_Type(namePrefix1)
print 'Content: %s' %DS.getDataStore_Content(namePrefix1)

namePrefix2 = '/adisorn/file2'
type = 'Text'
filename = '/home/adisorn/test2.txt'
DS.putDataStore(namePrefix2, type, filename)
#print DS.table
print 'add content name: %s' %namePrefix2
print 'Content type: %s' %DS.getDataStore_Type(namePrefix2)
print 'Content: %s' %DS.getDataStore_Content(namePrefix2)


DS.creaDataStore_json(DS.table)

# test = DS.readDataStore_json()
# pprint(test)
#
# print test[namePrefix2]['Content']
exitFlag = 0
print "Test Producer"
thread1 = producerThread(1, "Thread-1", 1, namePrefix1, DS)
thread2 = producerThread(2, "Thread-2", 2, namePrefix2, DS)

thread1.start()
thread2.start()


print "Exiting Main Thread"


# try:
#     #thread.start_new_thread(producer1.run())
#     thread.start_new_thread(Producer, ('/ndn/test1'))
#     thread.start_new_thread(Producer, ('/ndn/test2'))
# except:
#     print "Error: unable to start thread"







