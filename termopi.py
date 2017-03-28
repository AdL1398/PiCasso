#!/usr/bin/python

"""
title           : termopi.py
description     : Displays the status of the resources (cpu load and memory usage) consumed by a Raspberry Pi
                  computer and the resources consumed by one or more containrs instantiated in the Pi.  
source          :
author          : Carlos Molina Jimenez
date            : 27 Mar 2017
version         : 1.0
usage           :
notes           :
compile and run : % python termopi.py
                :   It imports pidict.py, dockerctl.py and picheck.py which are found in
                :   ./modules.
                :   You need to include "./modules" in the PYTHONPATH environment variable to
                :   indicate python where to find the pidict.py, dockerctl.py and picheck.py.
                :   For example, in a bash shell, you need to include the following lines
                :   in your .bash_profile file located in you home directory (you can see it with
                :   (# ls -la).
                :
                : PYTHONPATH="./modules"
                : export PYTHONPATH
python_version  : Python 2.7.12
====================================================
"""

import sys
import time
import os
import pidict     # functions for manipulating a dictionary data structure.
import picheck    # functions to get resources from the Raspberry Pi computer
import dockerctl  # functions to get resources from containers running in the Pi 

pi_status_default= {
    'PiID': 'SEG_1',
    'PiIP': '192.0.0.2',
    'hardResources': {'cpu': 'A 1.2GHz 64-bit quad-core ARMv8 CPU', 'mem': '2 GB', 'disk': '8 GB'},
    'softResources': {'OS': 'Linux'},
    'resourceUsage': {'cpuUsage': '32', 'cpuLoad': '2', 'memUsage':'20'},
    'containers':    [{'id':             '64c1f6e0e5c19f_2_1',
                       'cpuUsage':       '50',
                       'memUsage':       '3636',
                       'name':           'web1',
                       'status':         'Up 39 second',
                       'image':          'hypriot/rpi-busybox-httpd:latest_p8080',
                       'port_host':      '8080',
                       'port_container': '80'}]
    }

class termopi():
    def __init__(self, pi_status= pi_status_default):

        self.pi_status = pi_status 
#       self.pi_status_dflt= pi_status # wrong: self.pi_status and self.pi_status are pointer pointing to the same obj 
        self.pi_status_dflt= pi_status_default # this is good and used for testing only



    
    def prt_pi_resources(self):
        pidict.put_hardResources_cpu(self.pi_status, 'A 1.2GHz 64-bit quad-core ARMv8 CPU')
        pidict.put_hardResources_mem(self.pi_status, '1 GB')
        pidict.put_hardResources_disk(self.pi_status, '16 GB')
        """
        Real time values collected from the /proc/stat of the Pi
        """
        pidict.put_resourceUsage_mem(self.pi_status, picheck.pi_memUsage())
        pidict.put_resourceUsage_cpuLoad(self.pi_status, picheck.pi_cpuLoad())
        pidict.put_resourceUsage_cpuUsage(self.pi_status, picheck.pi_cpuUsage())
        dockerctl.get_container_info(self.pi_status)
      
        print(">>>>>BEGING THE RESOURCES OF THE PI<<<<<") 
        pidict.prt_allResources_of_a_pi(self.pi_status)
        print(">>>>>END THE RESOURCES OF THE PI<<<<<") 
                                         

if __name__ == '__main__':

 t= termopi()
 t.prt_pi_resources()
 
