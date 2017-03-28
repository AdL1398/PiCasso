"""
title           : pidict.py
description     : includes 
                  a) functions to manipulate a dictionary that representes 
                     the consumption of a Raspberry Pi resources
                  b) functions for creating a json file from the dictionary and 
                     reading it from the file and converting it back to the original 
                     dictionary
source          :  
author          : Carlos Molina Jimenez
date            : 15 Feb 2017
version         : 1.0
usage           : 
notes           :
compile and run : % python pidict.py
python_version  : Python 2.7.12   
====================================================
"""

"""
pi_status:     describes the resource configuration of an idividual Pi
               and their current consumption.
hardResources: hardware configuration of the Pi
               cpu: cpu description
               mem: memory size of the Pi in Gbytes
               disk disk size of the Pi in Gbutes
softResources: software configuration of the Pi
               OS: operating system of the Pi
resourceUsage: current status of resource consuption of the Pi
               cpuUsage: current cpu usage of the Pi in percentage
               cpuLoad:  current cpu load of the Pi (sa number between 1 and 4)
containers:    a dynamically growing/shrinking list of the containers currently running in the Pi.
               id: identification number of the container
               cpuUsage: current cpu usage of the container identified by id
               cpuUsage: current mem usage of the container identified by id

pi_status= {
    'PiID': '192.0.0.1',
    'hardResources': {'cpu': 'A 1.2GHz 64-bit quad-core ARMv8 CPU', 'mem': '1', 'disk': '32'}, 
    'softResources': {'OS': 'Linux'},
    'resourceUsage': {'cpuUsage': '30', 'cpuLoad': '70', memUsage:'20'},
    'containers':    [{'id': '64c1f6e0e5c19f9da2', 'cpuUsage': '23', 'memUsage': '3636', 'name': 'web1','status': 'Up 39 second', 'image': 'hypriot/rpi-busybox-httpd:latest'}
                     ]
}
"""

import json




#
# Default values to be checked
port_host_def= '8080',           
port_container_def= '8081'



"""
Expects a dictionary that representes the resources of a Pi and
the type of the cpu of the Pi.
Records the cpu in dicionary.
"""
def put_hardResources_cpu(pi_status,cpu):  
    pi_status['hardResources']['cpu']=cpu


"""
Expects a dictionary that representes the resources of a Pi.
and the size of the memory of the Pi and records it in the
dictionary.
"""
def put_hardResources_mem(pi_status,mem):        
    pi_status['hardResources']['mem']=mem


"""
Expects a dictionary that representes the resources of a Pi and
the size of the disk of the Pi.
Records the size of the disk in dictionary.  
"""
def put_hardResources_disk(pi_status,disk):        
    pi_status['hardResources']['disk']=disk

"""
Expects a dictionary that representes the resource usage of a Pi
Records the cpu usage in dictionary.
"""
def put_resourceUsage_cpuUsage(pi_status,cpu):
    pi_status['resourceUsage']['cpuUsage']=cpu


"""
Expects a dictionary that representes the resource usage of a Pi
Records the cpu load in dictionary.
"""
def put_resourceUsage_cpuLoad(pi_status,cpuLoad):
    pi_status['resourceUsage']['cpuLoad']=cpuLoad


"""
Expects a dictionary that representes the resource usage of a Pi
Records the memory usage in dictionary.
"""
def put_resourceUsage_mem(pi_status,mem):
    pi_status['resourceUsage']['memUsage']=mem


"""
Expects a dictionary that representes the resources of a Pi.
Returns a list of tuples. Each tuple has the form (containerID, cpuUsage, memUsage, name,
status, image) which represents the current status of each container as
designed by Adisorn (22 Feb 2017).
"""
def get_allResources_of_allContainers_of_Pi(pi_status):
    containersLst=pi_status['containers']
    l= len(containersLst)
    lst_of_tuples=[]
    for i in range(l):
        lst_of_tuples.append( (containersLst[i]['id'],      containersLst[i]['cpuUsage'],
                              containersLst[i]['memUsage'], containersLst[i]['name'],
                              containersLst[i]['status'],   containersLst[i]['image'],
                              containersLst[i]['port_host'],   containersLst[i]['port_host'],
                              containersLst[i]['port_container'],   containersLst[i]['port_container'])) 
    return lst_of_tuples




"""
Expects a dictionary that representes the resources of a Pi.
Prints all the resources of the Pi and returns None. 
"""
def prt_allResources_of_a_pi(pi_status):
    print("\n\nPiID: " + pi_status['PiID'])
    print("   PiIP:           " + pi_status['PiIP'])
    print("   hardResources:  " +  " cpu:  " + pi_status['hardResources']['cpu'] + 
                                " mem:  " + pi_status['hardResources']['mem'] +
                                " disk: " + pi_status['hardResources']['disk'])
    print("   sotfResources: "  +  " OS:   " + pi_status['softResources']['OS'])
 
    print("   resourceUsage: "  +  " cpuUsage: "  + pi_status['resourceUsage']['cpuUsage'] + 
                                " cpuLoad:  "  + pi_status['resourceUsage']['cpuLoad'] +
                                " memUsage: "  + pi_status['resourceUsage']['memUsage'])
  
    containersLst=get_allResources_of_allContainers_of_Pi(pi_status)
    for lst in containersLst:
        print("   containerID: "      + lst[0])
        print("        cpuUsage: "         + lst[1])
        print("        memUsage: "         + lst[2])
        print("        name: "             + lst[3])
        print("        status: "           + lst[4])
        print("        port_host "         + lst[5])
        print("        port_container "    + lst[6])
    return


