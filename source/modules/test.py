
from dataStore import DataStore
import os

import pidict
import json

# script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
# script_dir = os.path.split(script_path)[0] #i.e. /path/to/dir/
# rel_path = "PIstatus/data.txt"
# abs_file_path = os.path.join(script_dir, rel_path)
#
# print abs_file_path
#
# namePrefix = '/adisorn/file1'
# type = 'File'
# filename = '/home/adisorn/test.txt'
#
# DS = DataStore()
# #print DS.table
#
#
# DS.putDataStore(namePrefix, type, filename)
# #print DS.table
# print 'add content name: %s' %namePrefix
# print 'Content type: %s' %DS.getDataStore_Type(namePrefix)
# print 'Content: %s' %DS.getDataStore_Content(namePrefix)
#
# pi_status= {
#     'PiID': 'SEG_1',
#     'PiIP': '192.0.0.2',
#     'hardResources': {'cpu': 'A 1.2GHz 64-bit quad-core ARMv8 CPU', 'mem': '2 GB', 'disk': '8 GB'},
#     'softResources': {'OS': 'Linux'},
#     'resourceUsage': {'cpuUsage': '32', 'cpuLoad': '2', 'memUsage':'20'},
#     'containers':    [{'id':             '64c1f6e0e5c19f_2_1',
#                        'cpuUsage':       '50',
#                        'memUsage':       '3636',
#                        'name':           'web1',
#                        'status':         'Up 39 second',
#                        'image':          'hypriot/rpi-busybox-httpd:latest',
#                        'port_host':      '8080',
#                        'port_container': '80'},
#
#                       {'id':             '99c1f6e0e5c19f_2_1',
#                        'cpuUsage':       '50',
#                        'memUsage':       '3636',
#                        'name':           'web1',
#                        'status':         'Up 39 second',
#                        'image':          'hypriot/rpi-nano-httpd:latest',
#                        'port_host':      '8081',
#                        'port_container': '80'},
#
#                       {'id':             '88c1f6e0e5c19f_2_1',
#                        'cpuUsage':       '50',
#                        'memUsage':       '3636',
#                        'name':           'web1',
#                        'status':         'Up 39 second',
#                        'image':          'hypriot/rpi-test-httpd:latest',
#                        'port_host':      '8083',
#                        'port_container': '80'}
#                       ]
#     }

import os


