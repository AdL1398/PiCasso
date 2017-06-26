from influxdb import InfluxDBClient

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'picasso')
client.create_database('picasso')

#result = client.query('select cpuUsage from pi_status;')
#print("Result: {0}".format(result))
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
result = client.query('select container_name from pi_status;')
print("Result: {0}".format(result))
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
    #result = client.query('select container_cpuUsage from pi_status;')
    #print("Result: {0}".format(result))

result = client.query('select container_memUsage from pi_status;')
print("Result: {0}".format(result))


