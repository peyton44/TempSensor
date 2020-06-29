import os
from time import sleep
import paho.mqtt.client as mqtt

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

temp_sensor = '/sys/bus/w1/devices/28-01192a3ab8bd/w1_slave'

#######     Connect MQTT    #############
def on_connect(client, userdata, flags, rc):
	client.subscribe("test")

client = mqtt.Client()
client.on_connect = on_connect

client.connect("192.168.40.246", 1883, 60)
#############################################

def read_temp_raw():
	f = open(temp_sensor, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():

	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		sleep(0.2)
		lines = read_temp_raw()

	temp_result = lines[1].find('t=')

	if temp_result != -1:
		temp_string = lines[1].strip()[temp_result + 2:]
		# Temperature in Celcius
		# temp = float(temp_string) / 1000.0
		# Temperature in Fahrenheit
		temp = ((float(temp_string) / 1000.0) * (9.0 / 5.0)) + 32.0
		client.publish("test", round(temp, 1))
		return round(temp, 1)

while True:
  print(read_temp())
  sleep(2)
