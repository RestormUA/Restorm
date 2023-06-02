import paho.mqtt.client as mqtt
import time
import json

def on_gas_price(client, userdata, msg):
    with open("prices.json", "r") as f:
        data = json.load(f)

    data["Gas_Price"] = msg.payload.decode()
    f = open("prices.json", "w")
    f.write(json.dumps(data, indent=4))
    f.close()

def on_energy_price(client, userdata, msg):
    with open("prices.json", "r") as f:
        data = json.load(f)

    data["Energy_Price"] = msg.payload.decode()
    f = open("prices.json", "w")
    f.write(json.dumps(data, indent=4))
    f.close()

broker_address = "192.168.1.101"
broker_port = 1883
username = "rpi"
password = "rpimqtt"

client = mqtt.Client()
client.username_pw_set(username, password)
client.connect(broker_address, broker_port)
client.message_callback_add("Gas_Price", on_gas_price)
client.message_callback_add("Energy_Price", on_energy_price)
client.subscribe("Gas_Price")
client.subscribe("Energy_Price")

client.loop_start()
time.sleep(1)
client.disconnect()
client.loop_stop()