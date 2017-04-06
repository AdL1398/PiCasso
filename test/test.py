#!/usr/bin/python
import os
import subprocess

def system_call(command):
    # for Python below 2.7
    #p = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    #return p.stdout.read()

    # work with Python 2.7 up
    p = subprocess.check_output(command, shell=True)
    return p


container_id = '1c23081178cf '
cmd = "docker stats %s --no-stream | grep %s | awk  \'{print $2}\' " %(container_id, container_id)
cpu_usage = system_call(cmd)
cmd = "docker stats %s --no-stream | grep %s | awk  \'{print $4}\' " %(container_id, container_id)
mem_usage_unit = system_call(cmd)
cmd = "docker stats %s --no-stream | grep %s | awk  \'{print $8}\' " %(container_id, container_id)
mem_usage = system_call(cmd)

#result = subprocess.check_output(cmd, shell=True)
#print result
print cpu_usage
print mem_usage

