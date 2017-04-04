# termopi 

Simple termometer that shows the status of the resources consumed by one or more containers instantiated in a Raspberry Pi computer.


**Related projects**

You might  like to have a look at 


## Goals 
To help a user of Raspberry Pi computer to visualise the current status of the memmory usage and cpu Load of his or her Pi as well as of the resources consumed by a containers instantiated in a the Pi.


## How to download, compile and execute in Raspian (Debian) 

```shell
git clone https://github.com/fogleman/Minecraft.git
cd sources 
python testtermopi.py
>>>>>BEGING THE RESOURCES OF THE PI<<<<<

PiID: SEG_1
   PiIP:           192.0.0.2
   hardResources:   cpu:  A 1.2GHz 64-bit quad-core ARMv8 CPU mem:  1 GB disk: 16 GB
   sotfResources:  OS:   Linux
   resourceUsage:  cpuUsage: 5.04037442781 cpuLoad:  0.29 memUsage: 10
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



