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
python termopi.py
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



