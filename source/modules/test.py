
from dataStore import DataStore

namePrefix = '/adisorn/file1'
type = 'File'
filename = '/home/adisorn/test.txt'

DS = DataStore()
#print DS.table


DS.putDataStore(namePrefix, type, filename)
#print DS.table
print 'add content name: %s' %namePrefix
print 'Content type: %s' %DS.getDataStore_Type(namePrefix)
print 'Content: %s' %DS.getDataStore_Content(namePrefix)

