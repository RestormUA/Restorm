import paho.mqtt.client as mqtt
import json

broker_address = "192.168.1.101"
broker_port = 1883
username = "rpi"
password = "rpimqtt"

client = mqtt.Client()
client.username_pw_set(username, password)
client.connect(broker_address, broker_port)
topic = "Mode"

with open("prices.json", "r") as f:
    data = json.load(f)

percentage = 0.2
client.publish(topic, '0' if (float(data["Energy_Price"])*percentage)>=float(data["Gas_Price"]) else '1')

client.disconnect()