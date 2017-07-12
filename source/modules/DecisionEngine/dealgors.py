"""
title           : algor.py
description     : includes 
                  a) functions for 
source          :  
author          : Carlos Molina Jimenez
date            : 18 Jun 2017
version         : 1.0
                : 19 Jun 2017-- I decided to put the functions
                  get_number_of_containers_of_pi(l_dict, PiID)
                  get_pis_with_cpuLoad(l_dict)
                  get_pis_with_min_cpuLoad(l_dict)
                  Back to the decision engine: dededata.py of the
                  termopi application.
                  
usage           : 
notes           :
compile and run : % 
python_version  : Python 2.7.12   
====================================================
"""

"""
pi_stat:     describes the resource configuration of an idividual Pi
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

pi_stat= {
    'PiID': '192.0.0.1',
    'hardResources': {'cpu': 'A 1.2GHz 64-bit quad-core ARMv8 CPU', 'mem': '1', 'disk': '32'}, 
    'softResources': {'OS': 'Linux'},
    'resourceUsage': {'cpuUsage': '30', 'cpuLoad': '70'},
    'containers':    [{'id': 'Cont0', 'cpuUsage': '23', 'memUsage': '3636'}
                     ]
}
"""

import json



"""
Counts the numbers of containers running in a Pi.
input:  
        l_dict: list of dictionaries with pi status 
        [pi_status_SEG1, pi_status_SEG2, ...]
        PiID: id of the Pi of interest.
return: an integer between 0 and N if the PiID is found in the
        list, -1 otherwise
"""
def get_number_of_containers_of_pi(l_dict, PiID):
    for pi in l_dict: # needs proection against PiID not found
        if (pi['PiID']== PiID):
           return (len(pi['containers']))
    return(-1)



"""
Finds the list the Pis and cpuLoad and orders the list min to max
input: 
    l_dict: list of dictionaries
return: list of tuples (PiID,cpuLoad): 
    [(PiID,cpuLoad), (PiID,cpuLoad), ....]
"""
def get_pis_with_cpuLoad(l_dict):
    lst=[]

    for pi in l_dict:
        PiID=     pi['PiID']  # get next Pi
        cpuLoad= int(pi['resourceUsage']['cpuLoad'])
        lst.append((PiID,cpuLoad)) 
    sorted_lst= sorted(lst, key=lambda tup: tup[1])
    return(sorted_lst)



"""
Finds the Pis with min cpuLoad 
input: 
    l_dict: list of dictionaries
return:  
    tuple (PiID,cpuLoad) where the PiID is the Pi with
    the min cpuLoad. PiID is not necessarily the only Pi
    with that cpuLoad.
"""
def get_pis_with_min_cpuLoad(l_dict):
    l= get_pis_with_cpuLoad(l_dict)
    return(l[0][0], l[0][1])



#def replicate_image(lst_exhausted_containers,l_dict):
#    for tu in l_pi:
#      print("PiId= " + tu[0][0] + " cpuLoad= " + tu[0][1]) 
#      PiID=    tu[0][0]
#      cpuLoad= tu[0][1]
#      for ele in tu[1]:
#          print ("containerId: " + ele[0] + " cpuUsage: "  + ele[1] +
#            " image: "       +ele[2] + " port_host: " + ele[3]) 
#       


