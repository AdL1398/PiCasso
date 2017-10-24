#!/usr/bin/env python2.7

"""
title           : dockerctl.py
description     : includes 
                  a) a module to control docker containers
                  b) collect information of running containers
source          :  
author          : Adisorn Lertsinsrubtavee 
date            : 15 Feb 2017
version         : 1.0
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
#import docker
from docker import Client
import os
import subprocess

script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
script_dir = os.path.split(script_path)[0] #i.e. /path/to/dir/
parent_dir = os.path.split(script_dir)[0]
SEG_repo_path = os.path.join(script_dir, parent_dir, 'ServiceExecution', 'SEG_repository')
ServiceExecution_path = os.path.join(script_dir, parent_dir, 'ServiceExecution')
assigned_port = list(range(8000, 8080))

serviceInfo = {
            'umobilestore.tar':{
                                  'image_name':'al1309/umobile-store-nano-rpi:latest',
                                  'port_host': 80,
                                  'port_container': 80,
                                  'type': 'singleWebContainer',
                                  'component': ['ubuntu.tar', 'python.tar', 'java.tar']},
            'uhttpd.tar':{
                                  'image_name': 'fnichol/uhttpd:latest',
                                  'port_host': 8081,
                                  'port_container': 80,
                                  'type': 'singleWebContainer',
                                  'component': ['debian.tar', 'python.tar', 'java.tar']},

            'cloudrone.tar.gz':{
                                  'image_name': 'none',
                                  'port_host': 'none',
                                  'port_container': 'none',
                                  'type': 'DockerCompose',
                                  'component': ['webserver.tar', 'dbmysql.tar']}
               }

## For Linux
client = Client(base_url='unix://var/run/docker.sock', version='auto')

#client = docker.APIClient(base_url='unix://var/run/docker.sock')
pulling_flag = False
path = "SEG_repository"
info = {}
container_list = []

def deployContainer(image_fileName, num_deployedContainer):
    docker_image_name = serviceInfo[image_fileName]['image_name']
    #docker_port_host = serviceInfo[image_fileName]['port_host']
    docker_port_host = get_freeport(num_deployedContainer)
    docker_port_container = serviceInfo[image_fileName]['port_container']

    if docker_port_host != None:
        print 'Check docker Image Name: %s ' % docker_image_name
        print 'Port Host: %d' % docker_port_host
        print 'Port Container %d' % docker_port_container

        if is_image_running(docker_image_name) == True:
            print 'Image: %s is already running' % docker_image_name
            print 'Start Replicating Image:%s' % docker_image_name
            if run_image(docker_image_name, docker_port_host, docker_port_container) == True:
                print 'Running docker image %s ...' % docker_image_name
                return 'done'
            else:
                print 'Error: Cannot run image %s' % docker_image_name
                return 'error'
        else:
            ##image is not running
            ##check docker client has this image or not
            print 'Image: %s is NOT running' % docker_image_name
            if has_image(docker_image_name) == True:
                ## has image but image is not running
                print 'Image: %s is already stored' % docker_image_name
                if run_image(docker_image_name, docker_port_host, docker_port_container) == True:
                    print 'Running docker image %s ...' % docker_image_name
                    return 'done'
                else:
                    print 'Error: Cannot run image %s' % docker_image_name
                    return 'error'

            elif has_imagefile(image_fileName) == True :
                print 'Load image from local repository'

                if (load_image(image_fileName)==True):
                    print 'Image %s is loaded' %image_fileName
                    if run_image(docker_image_name, docker_port_host, docker_port_container) == True:
                        print 'Running docker image %s ...' % docker_image_name
                        return 'done'
                    else:
                        print 'Error: Cannot run image %s' % docker_image_name
                        return 'error'
            else:
                print 'Image: %s is not stored, pull from SC' % docker_image_name
                ### Call sendNextInterest to SC
                #prefix.requestService = (self.prefix_serviceMigration.append(Name(fileName)))
                return 'pull_image'
    else:
        print 'Cannot deploy a new container'
        return 'error'

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

def load_image(image_filename):
    #image_shortname = image_name[image_name.find("/") + 1:image_name.find(":")]
    #print image_shortname
    #f = open(path + '/'+ image_shortname + '.tar', 'r')
    #image_filename = serviceInfo[image_name]['image_filename']
    imagefile_path = os.path.join(SEG_repo_path, image_filename)
    print 'Path to image file %s' %imagefile_path
    f = open(imagefile_path, 'r')
    client.load_image(f)
    pulling_flag = False
    print 'image loaded'
    return True

def has_imagefile(image_filename):
    imagefile_path = os.path.join(SEG_repo_path, image_filename)
    if os.path.exists(imagefile_path) == True:
        print 'image file is already stored'
        return True
    else:
        print 'image file is not available in SEG repository'
        return False

def get_ExecutionType(image_filename):
    type = serviceInfo[image_filename]['type']
    return type

def has_ServiceInfo(image_filename):
    if image_filename in serviceInfo:
        return True
    else:
        return False

def run_DockerCompose_source (image_filename):
    imagefile_path = os.path.join(SEG_repo_path, image_filename)
    folder_name = image_filename.replace('.tar.gz', '')
    dockerCompose_source_path = os.path.join(SEG_repo_path, folder_name)
    print 'docker compose path %s' %dockerCompose_source_path
    if os.path.exists(dockerCompose_source_path) == True:
        print 'Docker compose source has already been extracted'
    else:
        print 'Extracting the source'
        cmd = 'tar -xzf ' + imagefile_path + ' -C ' + SEG_repo_path
        os.system(cmd)
    print 'run service: %s' %folder_name
    cmd = ServiceExecution_path + '/run_dockercompose.sh ' + dockerCompose_source_path
    print cmd
    os.system(cmd)

def get_freeport(num_con):
    if num_con+1 < len(assigned_port):
        free_port = assigned_port[num_con+1]
        print 'Free port = %d' %free_port
        free_port = assigned_port[num_con+1]
        return free_port
    else:
        print 'Run out of port'
        return None

def get_container_info(pi_status):
    """
    Expects a dictionary data structure that include keys and values of the
      parameters that describe the containers running in a Raspberry Pi computer.
    Returns the input dictionary populated with values measured from the current
      status of one or more containers running in the Pi.  
    """
    pi_status['containers'] = []
    for container in client.containers():
        cmd = "docker stats %s --no-stream | grep %s | awk  \'{print $2}\' " % (container['Id'], container['Id'])
        cpuUsage = system_call(cmd)
        cpuUsage_str = cpuUsage.replace("\n", "")
        cpuUsage_str = cpuUsage_str.replace("%", "")

        cmd = "docker stats %s --no-stream | grep %s | awk  \'{print $6}\' " % (container['Id'], container['Id'])
        memUsage = system_call(cmd)
        memUsage_str = memUsage.replace("\n", "")
        memUsage_str = memUsage_str.replace("%", "")
        #dict_port_host= container['Ports'][0]
        #p_int=dict_port_host['PublicPort']
        #port_host_str= str(p_int).replace("\n", "")

        new_container={
                       'id':             container['Id'],
                       'cpuUsage':       cpuUsage_str,
                       'memUsage':       memUsage_str,
                       'name':           container['Names'][0], # the client.container() returns a list of names.
                       'status':         container['Status'],   # as a temporary solution, I take the first name
                       'image':          container['Image'],    # of the list.
                       'port_host':      '80',         # the client.container() returns a list of ports
                       'port_container': '8000'}             # getting the first, is a tmp solution
        pi_status['containers'].append(new_container)
    return (len((pi_status['containers'])))


def system_call(command):
    # for Python below 2.7
    #p = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    #return p.stdout.read()

    # work with Python 2.7 up
    p = subprocess.check_output(command, shell=True)
    return p

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

