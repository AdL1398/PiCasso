import json
import os
import modules.tools.dockerctl
import os
import time
#from modules.DataStore.dataStore import DataStore
from modules.tools import dockerctl
from modules.tools import pidict

# dataSegmentNum = 0
# lastSegmentNum = 9
# TotalNumChunks = lastSegmentNum +1
# receivedContentChunk = [0 for i in range(TotalNumChunks)]
# print receivedContentChunk
# # receivedContentChunk[1] = 1
# # receivedContentChunk[5] = 1
# # receivedContentChunk[8] = 1
# #
# # for i in range(10):
# #     print ('index %d: %d' %(i,receivedContentChunk[i]))
# #
# #
# # numsum = sum(list(receivedContentChunk))
# # print ('Total received packets: %d' %(sum(list(receivedContentChunk))))
# stop = False
# while stop==False:
#     input = raw_input('Received chunkID: ')
#     dataSegmentNum = int(input)
#     receivedContentChunk[dataSegmentNum] = 1
#
#     if dataSegmentNum == lastSegmentNum:
#         print 'Received last chunk of content'
#         print 'Stop Sending Interest'
#
#     TotalReceivedChunk = sum(list(receivedContentChunk))
#     if TotalReceivedChunk == TotalNumChunks:
#         print 'Receive all the chunks'
#         stop = True


# ServiceExecution_path = '~/PiCasso/source/modules/ServiceExecution/'
# ServiceExecution_path = '~/PiCasso/source/modules/ServiceExecution/'
# dockerCompose_source_path = '~/PiCasso/source/modules/ServiceExecution/SEG_repository/cloudrone_WestCambridge'
# cmd = ServiceExecution_path + '/run_dockercompose.sh ' + dockerCompose_source_path
# print cmd
# os.system(cmd)




# def test_multireturn (x):
#     a = x +1
#     b = True
#     return a, b
#
# number, boo = test_multireturn(1)1
# print number
# print boo
#
#
# script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
# script_dir = os.path.split(script_path)[0] #i.e. /path/to/dir/
# #parent_dir = os.path.dirname(os.path.normpath(script_dir))
# parent_dir = os.path.split(script_dir)[0]
#
# image_filename = 'uhttpd.tar'
# imagefile_path = os.path.join(script_dir, parent_dir, 'ServiceExecution', 'SEG_repository', image_filename)
# print 'parent dir %s', parent_dir
# print 'target dir %s', imagefile_path
#
# if os.path.exists(imagefile_path) == True:
#    print 'image file is already stored'
# else:
#    print 'image file is not here'
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
#                        'image':          'hypriot/rpi-busybox-httpd:latest_p8080',
#                        'port_host':      '8080',
#                        'port_container': '80'}]
#     }
#
#
# dockerctl.get_container_info(pi_status)
# print(">>>>>BEGING THE RESOURCES OF THE PI<<<<<")
# pidict.prt_allResources_of_a_pi(pi_status)
# print(">>>>>END THE RESOURCES OF THE PI<<<<<")

script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
script_dir = os.path.split(script_path)[0] #i.e. /path/to/dir/
filename = 'nginx.tar.txt'
outputfile_path = os.path.join(script_dir, filename)

#print time.strftime("%a, %d %b %Y %X +0000", time.gmtime())
print time.ctime()
print time.time()
if os.path.exists(outputfile_path) == True:
    print 'output file is already existed'
else:
    print 'create output file'
    open(outputfile_path, 'a').close()

file = open(outputfile_path, 'a')

file.write('Start:  ' + time.ctime() +'\n')
file.write('Finish: '+ str(time.time()) +'\n')
file.close()


# assigned_port = list(range(8000, 8080))
# print 'port 0 %i' %assigned_port[0]
# print 'port 1 %i' %assigned_port[1]
#
# free_port = modules.tools.dockerctl.get_freeport(1)
# print 'free port %d' %free_port
# print 'len %d' %len(assigned_port)
# print 'last port %d' %assigned_port[80]

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




