"""
title           : picheckp.py
description     : Collect the resource usage (mem, cpu load and cpu usage of a Pi 
                :  Returns the values as strings.
                :   
author          : Adisorn Lertsinsrubtavee 
                : Carlos Molina Jimenez
                : 27 Feb 2017
                : Version 1.0
contributors    : Carlos Molina-Jimenez
                : 4 Mar 2017
                : Version 1.1
compile and run : % python picheck.py 
python_version  : Python 2.7.12
usage           : It is a component of a service migration platform 
notes           :
====================================================
"""

import os


"""
Return the memory usage of the Pi after converting it into a string
"""
def pi_memUsage():
    f = os.popen('cat /proc/meminfo | grep MemFree | awk \'{print $2}\'')
    memFree = f.read()
    f = os.popen('cat /proc/meminfo | grep MemTotal: | awk \'{print $2}\'')
    memTotal = f.read()
    memUsagePercent = (int(memTotal) - int(memFree)) * 100 / int(memTotal)
    memU_str= str(memUsagePercent).replace("\n","")
    return (memU_str) #Carlos changed the return to str 4Mar2017


"""
Returns the cpu load of the Pi after converting it into a string
"""
def pi_cpuLoad():
    f = os.popen("cat /proc/loadavg  | awk \'{print $2}\' ")
    loadavg = f.read()
    loadavg_str=  loadavg.replace("\n", "")
    return (str(loadavg_str)) #Carlos changed the return to str 4Mar2017


"""
Return the cpu usage of the Pi after converting it into a string
"""
def pi_cpuUsage():
    f = os.popen("cat /proc/stat | grep \'cpu \'  | awk \'{print $2}\' ")
    user = f.read()
    f = os.popen("cat /proc/stat | grep \'cpu \'  | awk \'{print $3}\'")
    nice = f.read()
    f = os.popen("cat /proc/stat | grep \'cpu \'  | awk \'{print $4}\'")
    system = f.read()
    f = os.popen("cat /proc/stat | grep \'cpu \'  | awk \'{print $5}\'")
    idle = f.read()
    f = os.popen("cat /proc/stat | grep \'cpu \'  | awk \'{print $6}\'")
    iowait = f.read()
    f = os.popen("cat /proc/stat | grep \'cpu \'  | awk \'{print $7}\'")
    irq = f.read()
    f = os.popen("cat /proc/stat | grep \'cpu \'  | awk \'{print $8}\'")
    softirq = f.read()
    f = os.popen("cat /proc/stat | grep \'cpu \'  | awk \'{print $9}\'")
    steal = f.read()
    f = os.popen("cat /proc/stat | grep \'cpu \'  | awk \'{print $10}\'")
    guest = f.read()
    f = os.popen("cat /proc/stat | grep \'cpu \'  | awk \'{print $11}\'")
    guest_nice = f.read()
    TotalCPU_time = float(user) + float(nice) + float(system) + float(idle) + float(iowait) + float(irq) + float(softirq) + float(steal)
    TotalCPU_Idle_time = float(idle) + float(iowait)
    TotalCPU_Usage_time = TotalCPU_time - TotalCPU_Idle_time
    TotalCPU_Usage_percentage = TotalCPU_Usage_time * 100 / TotalCPU_time
    TotalCPU_str= str(TotalCPU_Usage_percentage).replace("\n","")
    return (TotalCPU_str) #Carlos changed the return to str 4Mar2017
