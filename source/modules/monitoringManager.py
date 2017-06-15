from influxdb import InfluxDBClient
import json
import os.path
import pidict

fname = "./PIstatus/piStatusSEG_1.json"

def writeToDB(data,index):
    json_body = [
        {
            "measurement": "pi_status",
                "tags": {
                    "host_name": pidict.get_PiID(data),
                    "host_ip":   pidict.get_PiIP(data),
                    "hardware": "RPI-3",
                    "OS": "hypriotOS",
                    "image_name": pidict.get_conImage(data, index),
                    "container_id": pidict.get_conID(data, index),
                    "container_name": pidict.get_conName(data, index),
                    "container_status": pidict.get_conStatus(data, index),
                },
                #"time": "2009-11-10T23:00:00Z",
                "fields": {
                    "cpuLoad":  float(pidict.get_resourceUsage_cpuLoad(data)),
                    "cpuUsage": float(pidict.get_resourceUsage_cpuUsage(data)),
                    "memUsage": float(pidict.get_resourceUsage_memUsage(data)),
                    "port_host": int(pidict.get_conPorthost(data, index)),
                    "port_container": int(pidict.get_conPort(data, index)),
                    "container_cpuUsage": float(pidict.get_conCpuUsage(data, index)),
                    "container_memUsage": float(pidict.get_conMemUsage(data, index))
                }
        }
    ]
    return json_body

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')

client.create_database('example')

data = pidict.read_jsonFile(fname)
print data
l = len(data['containers'])
for i in range(l):
    client.write_points(writeToDB(data, i))

# result = client.query('select cpuUsage from pi_status;')
# print("Result: {0}".format(result))
#
# result = client.query('select memUsage from pi_status;')
# print("Result: {0}".format(result))
#
# result = client.query('select cpuLoad from pi_status;')
# print("Result: {0}".format(result))
#
# result = client.query('select image_name from pi_status;')
# print("Result: {0}".format(result))
#
# result = client.query('select container_id from pi_status;')
# print("Result: {0}".format(result))
#
#result = client.query('select container_name from pi_status;')
#print("Result: {0}".format(result))
#
# result = client.query('select container_status from pi_status;')
# print("Result: {0}".format(result))
#
# result = client.query('select port_host from pi_status;')
# print("Result: {0}".format(result))
#
# result = client.query('select port_container from pi_status;')
# print("Result: {0}".format(result))
#
result = client.query('select container_cpuUsage from pi_status;')
print("Result: {0}".format(result))

result = client.query('select container_memUsage from pi_status;')
print("Result: {0}".format(result))


