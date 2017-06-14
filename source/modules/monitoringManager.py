from influxdb import InfluxDBClient
import json
import os.path
import pidict


fname = "piStatusSEG_1.json"
path = "./PIstatus/"

def readMonitoringData(path, fname):
    json_data = path + fname
    with open(json_data) as json_infile:
        ds_loaded = json.load(json_infile)
    return ds_loaded

def writeDB():
    data = readMonitoringData(path, fname)
    print "Data from json file: ", data
    container_info = data['containerID']
    print container_info

    json_body = [
        {
            #"measurement": "cpu_load_short",
            # "tags": {
            #     "host": "server01",
            #     "region": "us-west"
            # },
            # "time": "2009-11-10T23:00:00Z",
            # "fields": {
            #     "value": 0.64
            # }
            "measurement": "pi_status",
                "tags": {
                    "host_name": pidict.get_PiID(data),
                    "host_ip":   pidict.get_PiIP(data),
                    "hardware": "RPI-3",
                    "OS": "hypriotOS",
                    "image_name": "influxdb:alpine",
                    "container_id": "b1761a9c073cec0893f7c63d0ebe06385ebc806b5b5f42458e5eb08775544669",
                    "container_name": "/love_newton"
                },
                "time": "2009-11-10T23:00:00Z",
                "fields": {
                    "cpuLoad":  pidict.get_resourceUsage_cpuLoad(data),
                    "cpuUsage": pidict.get_resourceUsage_cpuUsage(data),
                    "memUsage": pidict.get_resourceUsage_memUsage(data),
                    "image_name": "influxdb:alpine",
                    "container_id": "b1761a9c073cec0893f7c63d0ebe06385ebc806b5b5f42458e5eb08775544669",
                    "container_name": "/love_newton",
                    "container_status": "Up About an hour",
                    "port_host": "8086",
                    "container_cpuUsage": "0.13%",
                    "container_memUsage": "0.18%"
                }
        }
    ]
    return json_body



client = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')

client.create_database('example')

client.write_points(writeDB())

result = client.query('select cpuUsage from pi_status;')
print("Result: {0}".format(result))

result = client.query('select memUsage from pi_status;')
print("Result: {0}".format(result))

result = client.query('select cpuLoad from pi_status;')
print("Result: {0}".format(result))
