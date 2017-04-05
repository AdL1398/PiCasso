# termopi  

Simple termometer that shows the status of the resources consumed by one or more containers instantiated in a Raspberry Pi computer.
 
 hshshshshshssh

**Related projects**

You might  like to have a look at 


## Goals 
To help a user of Raspberry Pi computer to visualise the current status of the memmory usage and cpu Load of his or her Pi as well as of the resources consumed by a containers instantiated in a the Pi.


## How to download, compile and execute in Raspian (Debian) 

```shell
# git clone https://github.com/fogleman/Minecraft.git

# cd sources 

# python testtermopi.py

>>>>>BEGING THE RESOURCES OF THE PI<<<<<

PiID: SEG_1
   PiIP:           192.0.0.2
   hardResources:   cpu:  A 1.2GHz 64-bit quad-core ARMv8 CPU mem:  1 GB disk: 16 GB
   sotfResources:  OS:   Linux
   resourceUsage:  cpuUsage: 1.1824101223 cpuLoad:  0.20 memUsage: 12
   containerID: 2b5ec65975ba0197f5ffae35eb726062fab50697125cbef304335036e62eb762
        cpuUsage: 126607127
        memUsage: 360448
        name: /Clare
        status: Up 19 seconds
        port_host hypriot/rpi-busybox-httpd:latest
        port_container 8006
   containerID: be1214ecf0008839eb92d70657a772a5fb2bf5466b5ec6873f7f076647822c61
        cpuUsage: 106020582
        memUsage: 192512
        name: /Bob
        status: Up 35 seconds
        port_host hypriot/rpi-busybox-httpd:latest
        port_container 8004
   containerID: 2e93d453da084131cd50dc41f91a712d7162154811b7ba5b811eaaf802abf73e
        cpuUsage: 105117922
        memUsage: 1773568
        name: /Peter
        status: Up About a minute
        port_host hypriot/rpi-busybox-httpd:latest
        port_container 8002
>>>>>END THE RESOURCES OF THE PI<<<<<


.....migration record in same Pi..............
................................................................


Nothing to replicate
len first l= 0len second l= 0

```

## How to instantiate containers 

- To see the containers currently running in the Pi
```shell
# docker ps  
```

- To create a container 
```shell
# docker run --name adisorn -d -p 8002:80 hypriot/rpi-busybox-httpd
```


- To delete a container 
```shell
# ... 
```

