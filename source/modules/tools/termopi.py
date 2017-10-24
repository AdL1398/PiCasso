#!/usr/bin/python

"""
title           : termopi.py
description     : Displays the status of the resources (cpu load and memory usage) consumed by a Raspberry Pi
                  computer and the resources consumed by one or more containrs instantiated in the Pi.  
source          :
author          : Adisorn Lertsinsrubtavee (Adisorn.Lertsinsrubtavee@cl.cam.ac.uk)
date            : 27 Mar 2017
institution     : Computer Laboratory, University of Cambridge
version         : 2.0
usage           :
notes           :
compile and run : % python termopi.py
                :   It imports dockerctl.py and picheck.py which are found in
                :   ./modules/tools.
                :   You need to include "./modules" in the PYTHONPATH environment variable to
                :   indicate python where to find the dockerctl.py and picheck.py.
                :   For example, in a bash shell, you need to include the following lines
                :   in your .bash_profile file located in you home directory (you can see it with
                :   (# ls -la).
                :
                : PYTHONPATH="./modules"
                : export PYTHONPATH
python_version  : Python 2.7.12
====================================================
"""

import os
import sys
import time
import json
import picheck     # functions to get resources from the Raspberry Pi computer
import pidict      # functions for manipulating a dictionary data structure.
from modules.misc.dedata import dedata # class with dictionary data structure
import dockerctl

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

"""
In this version the dictionary is populated and stored on disk as a json file and
read from disk for analysis
"""
jsonpathdefault= "./PIstatus/"                # path of folder with json file
jsonfnamedefault="pi_status.json"             # json file with resource status of Pi and containers
migrationfname= "migrationFile.json"          # json file with info to replicate containers
cpuUsageThreshold= 50

class termopi():
    def __init__(self, pi_status=pi_status_default, 
                       jsonpath=jsonpathdefault, 
                       jsonfname=     jsonfnamedefault):

        self.pi_status = pi_status 
        self.pi_status_dflt= pi_status_default # this is good and used for testing only
        self.jsonpath= jsonpath
        self.jsonfname= jsonfname


    
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
                                         
    def create_jsonfile_with_pi_status(self, filename, node_name):
        import os.path

        self.pi_status['hardResources']['cpu'] = 'A 1.2GHz 64-bit quad-core ARMv8 CPU'
        self.pi_status['hardResources']['mem'] = '1 GB'
        self.pi_status['hardResources']['disk'] = '32 GB'
        self.pi_status['PiID'] = node_name
        """
        Real time values collected from the /proc/stat of the Pi
        """
        self.pi_status['resourceUsage']['memUsage'] = picheck.pi_memUsage()
        self.pi_status['resourceUsage']['cpuLoad'] = picheck.pi_cpuLoad()
        self.pi_status['resourceUsage']['cpuUsage'] = picheck.pi_cpuUsage()
        dockerctl.get_container_info(self.pi_status)
        self.create_jsonFile(self.pi_status, filename)

    def check_pi_resource_status(self, cpuUsageThreshold):
        mydedata= dedata(self.jsonpath)

        print("\n\n.....migration record in same Pi..............")
        l_re= mydedata.replicate_cpuUsageExhaustedContainers(cpuUsageThreshold,)

        print("len first l= " + str(len(l_re[0]))  + "len second l= " + str(len(l_re[1])))

    def response_interest_monitoring(self):
        print "Check Pi and Containers Status"
        self.prt_pi_resources()
        print "Update json file"
        self.create_jsonfile_with_pi_status()

    def create_jsonFile(self, pi_stat, fname):
        try:
            os.remove(fname)
        except OSError:
            pass
        with open(fname, 'w') as json_outfile:
            json.dump(pi_stat, json_outfile, ensure_ascii=False)
        return

