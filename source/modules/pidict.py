"""
title           : pidict.py
description     : includes
                  a) functions to manipulate a dictionary that representes
                     the consumption of a Raspberry Pi resources
                  b) functions for creating a json file from the dictionary and
                     reading it from the file and converting it back to the original
                     dictionary
source          :
author          : Carlos Molina-Jimenez (Carlos.Molina@cl.cam.ac.uk)
date            : 15 Feb 2017
institution     : Computer Laboratory, University of Cambridge
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
Expects a dictionary that representes the resources of a Pi.
Returns the id of the Pi
"""
def get_PiID(pi_stat):
    piID=pi_stat['PiID']
    return piID

"""
Expects a dictionary that representes the resources of a Pi and
the id of the Pi. Records the id in the dictionary.
"""
def put_PiID(pi_stat,piID):
    pi_stat['PiID']=piID
    return


"""
Expects a dictionary that representes the resources of a Pi and
the IP address of the Pi. Records the id in the dictionary.
"""
def put_PiIP(pi_stat,piIP):
    pi_stat['PiIP']=piIP
    return

"""
Expects a dictionary that representes the resources of a Pi.
Returns the IP address of the Pi
"""
def get_PiIP(pi_stat):
    piIP=pi_stat['PiIP']
    return piIP

"""
Expects a dictionary that representes the resources of a Pi.
Returns a sub-dictionary that represents the hardware resources of the Pi.
"""
def get_hardResources(pi_stat):
    hardRes=pi_stat['hardResources']
    return hardRes 

"""
Expects a dictionary that representes the resources of a Pi.
Returns the type of the cpu the Pi. 
"""
def get_hardResources_cpu(pi_stat):            
    cpu=pi_stat['hardResources']['cpu']
    return cpu 

"""
Expects a dictionary that representes the resources of a Pi and
the type of the cpu of the Pi.
Records the cpu in dicionary.
"""
def put_hardResources_cpu(pi_stat,cpu):  
    pi_stat['hardResources']['cpu']=cpu
    return

"""
Expects a dictionary that representes the resources of a Pi.
Returns the size of the memory of the Pi 
"""
def get_hardResources_mem(pi_stat):            
    mem=pi_stat['hardResources']['mem']
    return mem 

"""
Expects a dictionary that representes the resources of a Pi.
and the size of the memory of the Pi and records it in the
dictionary.
"""
def put_hardResources_mem(pi_stat,mem):        
    pi_stat['hardResources']['mem']=mem
    return

"""
Expects a dictionary that representes the resources of a Pi.
Returns the size of the disk of the Pi 
"""
def get_hardResources_disk(pi_stat):
    disk=pi_stat['hardResources']['disk']
    return  disk 

"""
Expects a dictionary that representes the resources of a Pi and
the size of the disk of the Pi.
Records the size of the disk in dictionary.  
"""
def put_hardResources_disk(pi_stat,disk):        
    pi_stat['hardResources']['disk']=disk
    return


"""
Expects a dictionary that representes the resource usage of a Pi
Records the cpu usage in dictionary.
"""
def put_resourceUsage_cpuUsage(pi_status,cpu):
    pi_status['resourceUsage']['cpuUsage']=cpu

def get_resourceUsage_cpuUsage(pi_status):
    cpuUsage = pi_status['resourceUsage']['cpuUsage']
    return cpuUsage

"""
Expects a dictionary that representes the resource usage of a Pi
Records the cpu load in dictionary.
"""
def put_resourceUsage_cpuLoad(pi_status,cpuLoad):
    pi_status['resourceUsage']['cpuLoad']=cpuLoad

def get_resourceUsage_cpuLoad(pi_status):
    cpuLoad = pi_status['resourceUsage']['cpuLoad']
    return cpuLoad

"""
Expects a dictionary that representes the resource usage of a Pi
Records the memory usage in dictionary.
"""
def put_resourceUsage_mem(pi_status,mem):
    pi_status['resourceUsage']['memUsage']=mem

def get_resourceUsage_memUsage(pi_status):
    memUsage = pi_status['resourceUsage']['memUsage']
    return memUsage




"""
Expects a dictionary that representes the resources of a Pi.
Returns a list of dictionaries where each dictionary represents
a container currently running in the Pi. 
"""
def get_containers(pi_stat):
    containersLst=pi_stat['containers']
    return containersLst 


"""
Expects a dictionary that representes the resources of a Pi.
Returns the number of containers currently running in the Pi 
"""
def get_numContainers(pi_stat):
    containerLst=pi_stat['containers']
    return len(containerLst) 

"""
Expects a dictionary that representes the resources of a Pi,
the id of a container and the resource of interest (cpu, mem or disk).
Returns the current status of the given resource
"""
def get_containerResource(pi_stat, containerID,resource):
    containersLst=pi_stat['containers']
    l= len(containersLst)
    if l==0:
       return "No containers"
    else:
       for i in range(l):
         if containersLst[i]['id']==containerID:
            return containersLst[i][resource] 
         else:
            return "containerID not found"

"""
Expects a dictionary that representes the resources of a Pi and
the id of a container.
Returns a tuple of the form (containerID, cpuUsage, memUsage) which
represents the current status of the container identified as containerID.
Returns ("0", "0", "0") if no container is found with containerID
"""
def get_containerResources(pi_stat, containerID):
    containersLst=pi_stat['containers']
    l= len(containersLst)
    for i in range(l):
      if containersLst[i]['id']==containerID:
         return (containersLst[i]['id'], containersLst[i]['cpuUsage'], containersLst[i]['memUsage']) 
      else:
         return ("0", "0", "0") 

"""
Expects a dictionary that representes the resources of a Pi and
a tuple of the form (containerID, cpuUsage, memUsage) which
represents the current status of the container identified as containerID,
produces a dictionary out of the tuple and appends it to tail of
the list of containers running in the Pi
"""
def put_container(pi_stat, containerID, cpuUsage, memUsage):
    containersList=pi_stat['containers']
    containersList.append({'id': containerID, 'cpuUsage': cpuUsage, 'memUsage': memUsage})
    return


"""
Expects a dictionary that representes the resources of a Pi.
Returns a list of tuples. Each tuple has the form (containerID, cpuUsage, memUsage) which
represents the current status of each container
"""
def get_allContainerResources(pi_stat):
    containersLst=pi_stat['containers']
    l= len(containersLst)
    lst_of_tuples=[]
    for i in range(l):
        lst_of_tuples.append( (containersLst[i]['id'], containersLst[i]['cpuUsage'], containersLst[i]['memUsage']) )
    return lst_of_tuples 





""" 
Expects a dictionary that representes the resources of a Pi
and a cpuUsageThreshold.
Returns the containers with exhausted cpuUsage, that is:
             cpuUsage > cpuUsageThreshold.
The return is a list of tuples:
[(containerID, cpuUsage), (containerID, cpuUsage), ...]
"""
def get_cpuUsageExhaustedConta_of_Pi(pi_stat,cpuUsageThreshold):
    contaLst=pi_stat['containers']
    lst_of_tuples=[]
    for c in contaLst:
        if (int(c['cpuUsage']) > cpuUsageThreshold):
           lst_of_tuples.append( (c['id'], c['cpuUsage']) )
    return lst_of_tuples 


"""
Expects a dictionary that representes the resources of a Pi
and a cpuUsageThreshold.
Returns the containers with vigorous cpuUsage, that is:
             cpuUsage <= cpuUsageThreshold.
The return is a list of tuples:
[(containerID, cpuUsage), (containerID, cpuUsage), ...]
"""
def get_cpuUsageVigorousConta_of_Pi(pi_stat,cpuUsageThreshold):
    contaLst=pi_stat['containers']
    lst_of_tuples=[]
    for c in contaLst:
        if (int(c['cpuUsage']) <= cpuUsageThreshold):
           lst_of_tuples.append( (c['id'], c['cpuUsage']) )
    return lst_of_tuples 



"""
Expects a dictionary that representes the resources of a Pi
and a cpuUsageThreshold.
Returns the containers with exhausted cpuUsage, that is:
             cpuUsage > cpuUsageThreshold.
The return is a list of tuples:
[(containerID, cpuUsage, image, port_host), (containerID, cpuUsage, image, port_host), ...]
"""
def get_cpuUsageExhaustedContainers_of_Pi(pi_stat,cpuUsageThreshold):
    contaLst=pi_stat['containers']
    lst_of_tuples=[]
    for c in contaLst:
        if (int(c['cpuUsage']) > cpuUsageThreshold):
           lst_of_tuples.append( (c['id'], c['cpuUsage'], c['image'], c['port_host']) )
    return lst_of_tuples 

"""
Expects a dictionary that representes the resources of a Pi
and a cpuUsageThreshold.
Returns the containers with NO exhausted cpuUsage, that is:
             cpuUsage <= cpuUsageThreshold.
The return is a list of tuples:
[(containerID, cpuUsage), (containerID, cpuUsage), ...]
"""
def get_cpuUsageVigorousContainers_of_Pi(pi_stat,cpuUsageThreshold):
    contaLst=pi_stat['containers']
    lst_of_tuples=[]
    for c in contaLst:
        if (int(c['cpuUsage']) <= cpuUsageThreshold):
           lst_of_tuples.append( (c['id'], c['cpuUsage'], c['image'], c['port_host']) )
#          lst_of_tuples.append( (c['id'], c['cpuUsage']) )
    return lst_of_tuples 




"""
Expects a dictionary that representes the resources of a Pi
and a cpuUsageThreshold.
Returns the list of all the containers running in the Pi ONLY if all 
of them are vigorous:
             cpuUsage <= cpuUsageThreshold
[(containerID, cpuUsage, image, port_host), (containerID, cpuUsage, image, port_host), ...]
Returns an empty list if at least one container is cpuUsage exhausted.
"""
def get_cpuUsageVigorousContainersOnly_of_Pi(pi_stat,cpuUsageThreshold):
    contaLst=pi_stat['containers']
    lst_of_tuples=[]
    for c in contaLst:
        if (int(c['cpuUsage']) <= cpuUsageThreshold):
           lst_of_tuples.append( (c['id'], c['cpuUsage'], c['image'], c['port_host']) )
        else:
           lst_of_tuples=[] 
    return lst_of_tuples 




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
        print("        containerID: "      + lst[0])
        print("        cpuUsage: "         + lst[1])
        print("        memUsage: "         + lst[2])
        print("        name: "             + lst[3])
        print("        status: "           + lst[4])
        print("        port_host "         + lst[5])
        print("        port_container "    + lst[6])
    return

"""
Functions written on 21 Feb 2017
Expects a dictionary that representes the resources of a Pi and
the id of a container.
Returns a tuple of the form (PiID, cpuUsage, cpuLoad, memUsage) which
represents the current status of the Pi identified as PiID.
"""
def get_resourceUsage(pi_status):
    return(pi_status['PiID'],  pi_status['resourceUsage']['cpuUsage'],
                               pi_status['resourceUsage']['cpuLoad'],
                               pi_status['resourceUsage']['memUsage'])



"""
Expects a dictionary that representes the resources of a Pi
and a fname.
1) Deletes fname if it already exists then
2) Creates a json file named fname. 
"""
def create_jsonFile(pi_stat, fname):
  import os
  try:
    os.remove(fname)
  except OSError:
    pass
  json_pi_stat = json.dumps(pi_stat)
  with open(fname, 'w') as json_outfile:
       json.dump(pi_stat, json_outfile, ensure_ascii=False)
  return



"""
Expects a dictionary that representes the resources of a Pi
and a file name that stores a json record that represents
the resources of a Pi.
Reads the json file from disk and converts it into the original dictionary 
that represents the resources of the Pi
"""
def read_jsonFile(fname):
    with open(fname) as json_infile:
         pi_stat_loaded = json.load(json_infile)
    return pi_stat_loaded


"""
Expects a dictionary before and after being loaded 
from a file where it was stored as a json object.
Compares the two versions and return true is they are
equal, false otherwise
"""
def test_json_retrieval(pi_stat, pi_stat_loaded):
    if (pi_stat == pi_stat_loaded):
       return "true"
    else:
       return "false"

def get_conID(pi_status, index):
    containerList = pi_status['containers']
    if index < len(containerList):
        return containerList[index]['id']
    else:
        return "None"

def get_conCpuUsage(pi_status, index):
    containerList = pi_status['containers']
    if index < len(containerList):
        return containerList[index]['cpuUsage']
    else:
        return "None"

def get_conMemUsage(pi_status, index):
    containerList = pi_status['containers']
    if index < len(containerList):
        return containerList[index]['memUsage']
    else:
        return "None"

def get_conName(pi_status, index):
    containerList = pi_status['containers']
    if index < len(containerList) :
        return containerList[index]['name']
    else:
        return "None"

def get_conStatus(pi_status, index):
    containerList = pi_status['containers']
    if index < len(containerList) :
        return containerList[index]['status']
    else:
        return "None"

def get_conImage(pi_status, index):
    containerList = pi_status['containers']
    if index < len(containerList) :
        return containerList[index]['image']
    else:
        return "None"

def get_conPorthost(pi_status, index):
    containerList = pi_status['containers']
    if index < len(containerList) :
        return containerList[index]['port_host']
    else:
        return "None"

def get_conPort(pi_status, index):
    containerList = pi_status['containers']
    if index < len(containerList) :
        return containerList[index]['port_container']
    else:
        return "None"
