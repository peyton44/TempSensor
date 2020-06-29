import os
from time import sleep
import paho.mqtt.client as mqtt
import random

topic = "test"
server = "192.168.40.246"
port = 1883

#######     Connect MQTT    #############
def on_connect(client, userdata, flags, rc):
	client.subscribe(topic)

client = mqtt.Client()
client.on_connect = on_connect

client.connect(server, port, 60)
#############################################

sensors = {
    "Freezer1" : 3,
    "Freezer2" : 0,
    "Freezer3" : -2,
    "Freezer4" : 1,
}

def publishTemp():
    for s in sensors:
        if random.randrange(5) == 1:
            if random.randrange(2) == 1:
                sensors[s] = sensors[s] + 1
            else:
                sensors[s] = sensors[s] - 1

        sensorTopic = "foodcity/tempSensor/" + s
        client.publish(sensorTopic, sensors[s])
        print(s, sensors[s])
        sleep(2)

while True:
  publishTemp()
