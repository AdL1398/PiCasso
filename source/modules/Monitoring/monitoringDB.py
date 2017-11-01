import json
import os.path
import threading
from influxdb import InfluxDBClient
from requests.exceptions import ConnectionError
from modules.tools import pidict


class InfluxDBWriter():

    def __init__(self, path, filename):
        self.fname = os.path.join(path, filename)
        print 'json file path', self.fname
        self.connected = False
        self.client = None
        #self.client = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')
        #self.client.create_database('example')

    def connect(self):
        #influxdb_url = os.environ['INFLUXDB_URL']
        #influxdb_port = os.environ['INFLUXDB_PORT']
        influxdb_url = 'localhost'
        influxdb_port = 8086
        print("Connecting to InfluxDB")
        self.client = InfluxDBClient(influxdb_url, influxdb_port, 'root', 'root', 'picasso')
        self.client.create_database('picasso')
        self.connected = True
        print("Connected to InfluxDB")

    def write(self):
        try:
            if (self.connected == False):
                self.connect()

            data = pidict.read_jsonFile(self.fname)
            print data
            l = len(data['containers'])
            for i in range(l):
                self.client.write_points(self.collectData(data, i))
            
        except ConnectionError as e:
            self.connected = False
            print("ERROR: Cannot connect to InfluxDB. Dropping data point. See exception below for details.")
            print(e)
        # except urllib2.HTTPError as e:
        #     InfluxDBWriter.connected = False
        #     print("ERROR: Database locust does not exist. Dropping data point. Will attempt to reconnect and create database.")
        # print(e)
            
    def collectData(self, data, con_index):
        json_body = [
            {
                "measurement": "pi_status",
                    "tags": {
                        "host_name": pidict.get_PiID(data),
                        "host_ip":   pidict.get_PiIP(data),
                        "hardware": "RPI-3",
                        "OS": "hypriotOS",
                        "image_name": pidict.get_conImage(data, con_index),
                        "container_id": pidict.get_conID(data, con_index),
                        "container_name": pidict.get_conName(data, con_index),
                        "container_status": pidict.get_conStatus(data, con_index),
                    },

                    "fields": {
                        "cpuLoad":  float(pidict.get_resourceUsage_cpuLoad(data)),
                        "cpuUsage": float(pidict.get_resourceUsage_cpuUsage(data)),
                        "memUsage": float(pidict.get_resourceUsage_memUsage(data)),
                        "port_host": int(pidict.get_conPorthost(data, con_index)),
                        "port_container": int(pidict.get_conPort(data, con_index)),
                        "container_cpuUsage": float(pidict.get_conCpuUsage(data, con_index)),
                        "container_memUsage": float(pidict.get_conMemUsage(data, con_index))
                    }
            }
        ]
        return json_body

