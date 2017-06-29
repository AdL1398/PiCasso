#!/usr/bin/python

"""
title           : testtermopi.py
description     : This program runs the termopi.py 
                : Displays the status of the resources (cpu load and memory usage) consumed by a Raspberry Pi
                  computer and the resources consumed by one or more containers instantiated in the Pi.  
source          :
author          : Carlos Molina-Jimenez (Carlos.Molina@cl.cam.ac.uk)
date            : 27 Mar 2017
institution     : Computer Laboratory, University of Cambridge
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

from modules.tools.termopi import termopi # class with dictionary data structure
# Threshold of cpu exhaustion
cpuUsageThreshold= 50
cpuLoadThreshold= 3

termo= termopi()
termo.prt_pi_resources()
termo.create_jsonfile_with_pi_status()
#termo.check_pi_resource_status(cpuUsageThreshold)

  
