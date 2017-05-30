
from dataStore import DataStore
import os

script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
script_dir = os.path.split(script_path)[0] #i.e. /path/to/dir/
rel_path = "PIstatus/data.txt"
abs_file_path = os.path.join(script_dir, rel_path)

print abs_file_path

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

