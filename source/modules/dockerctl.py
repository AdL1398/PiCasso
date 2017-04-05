#!/usr/bin/env python2.7

"""
title           : pidict.py
description     : includes 
                  a) functions to collect the current status of the resources
                     consumed by containers instantiated in a Raspberry Pi
                     computer. 
source          :  
author          : Adisorn Lertsinsrubtavee 
date            : 15 Feb 2017
version         : 1.0
contributors    : Carlos Molina-Jimenez
usage           :  
notes           :
compile and run : It is a python module imported by a main python programme. 
python_version  : Python 2.7.12 
====================================================
"""

# dictionary data structure
# pi_status= {
#     'PiID': '192.0.0.1',
#     'hardResources': {'cpu': 'A 1.2GHz 64-bit quad-core ARMv8 CPU', 'mem': '1', 'disk': '32'},
#     'softResources': {'OS': 'Linux'},
#     'resourceUsage': {'cpuUsage': '30', 'cpuLoad': '70'},
#     'containers':    []
#     }



import time
import docker
#from docker import Client
import os

client = docker.APIClient(base_url='unix://var/run/docker.sock',version='auto')
#client = docker.from_env(assert_hostname=False)
pulling_flag = False
path = "SEG_repository"
info = {}
container_list = []


def run_image(image_name, port_host, port_container):
    print time.strftime("%a, %d %b %Y %X +0000", time.gmtime())
    if has_image(image_name) == True:
        print 'Start running image'
        config = client.create_host_config(port_bindings={port_container:port_host})
        container = client.create_container(image=image_name, ports=[port_container], host_config=config)
        client.start(container=container.get('Id'))
        print 'running image'
        print time.strftime("%a, %d %b %Y %X +0000", time.gmtime())
        return is_image_running(image_name)
    print time.strftime("%a, %d %b %Y %X +0000", time.gmtime())
    return False


def has_image(image_name):
    local_images = client.images()
    for image in local_images:
        #print image["RepoTags"]
        if image_name in image["RepoTags"]:
            print "HAS image: %s" % image["RepoTags"]
            return True
    return False


def is_image_running(image_name):
    for container in client.containers():
        if container["Image"] == image_name:
            return True
    return False


def load_image(image_name):
    image_shortname = image_name[image_name.find("/") + 1:image_name.find(":")]
    print image_shortname
    f = open(path + '/'+ image_shortname + '.tar', 'r')
    client.load_image(f)
    pulling_flag = False
    print 'image loaded'


def get_container_info(pi_status):
    """
    Expects a dictionary data structure that include keys and values of the
      parameters that describe the containers running in a Raspberry Pi computer.
    Returns the input dictionary populated with values measured from the current
      status of one or more containers running in the Pi.  
    """
    pi_status['containers']=[]
    for container in client.containers():
        with open('/sys/fs/cgroup/cpuacct/docker/' + container['Id'] + '/cpuacct.usage', 'r') as f:
            cpuUsage = f.readline()
            cpuUsage_str= cpuUsage.replace("\n", "")

        with open('/sys/fs/cgroup/memory/docker/' + container['Id'] + '/memory.usage_in_bytes', 'r') as f:
            memUsage = f.readline()
            memUsage_str= memUsage.replace("\n", "")

        dict_port_host= container['Ports'][0]
        p_int=dict_port_host['PublicPort'] 
        port_host_str= str(p_int).replace("\n", "")

        new_conta={
                       'id':             container['Id'],
                       'cpuUsage':       cpuUsage_str,
                       'memUsage':       memUsage_str,
                       'name':           container['Names'][0], # the client.container() returns a list of names.
                       'status':         container['Status'],   # as a temporary solution, I take the first name
                       'image':          container['Image'],    # of the list.
                       'port_host':      port_host_str,         # the client.container() returns a list of ports
                       'port_container': '80'}             # getting the first, is a tmp solution
        pi_status['containers'].append(new_conta)
    return (len((pi_status['containers'])))



def container_info(pi_status):
    pi_status['containers']=[]
    for container in client.containers():
        with open('/sys/fs/cgroup/cpuacct/docker/' + container['Id'] + '/cpuacct.usage', 'r') as f:
            cpuUsage = f.readline()
        with open('/sys/fs/cgroup/memory/docker/' + container['Id'] + '/memory.usage_in_bytes', 'r') as f:
            memUsage = f.readline()
        new_conta={
                       'id':             container['Id'],
                       'cpuUsage':       cpuUsage,
                       'memUsage':       memUsage,
                       'name':           container['Names'][0], # this is a list of names, I us the first 
                       'status':         container['Status'],   # name of the list. <-- short cut!!!
                       'image':          container['Image'],
                       'port_host':      container['Ports'][0], 
                       'port_container': '80'} 

        pi_status['containers'].append(new_conta)
        print("\n\n++++++ conta lst len= " + str (len(pi_status['containers'])) + "after append +++++")
    return (len((pi_status['containers'])))


def container_info_ori(pi_status):
    for container in client.containers():
        with open('/sys/fs/cgroup/cpuacct/docker/' + container['Id'] + '/cpuacct.usage', 'r') as f:
            cpuUsage = f.readline()
        with open('/sys/fs/cgroup/memory/docker/' + container['Id'] + '/memory.usage_in_bytes', 'r') as f:
            memUsage = f.readline()
        putgetfunc.put_container(pi_status, container['Id'], cpuUsage, memUsage, container['Names'], container['Status'], container['Image'])
    return pi_status
