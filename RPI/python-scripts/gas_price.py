import paho.mqtt.client as mqtt
from requests import get
import urllib3
import json
urllib3.disable_warnings()

def getGasPrice():
    urlHomeAssistant = "http://192.168.1.101:8123/"
    entityID = "input_text.gas_price_eur_kw"

    # Access token created through Home Assistant profile
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIxYzljODRhMzI5NjU0MzUwYjc4YWZkMzdlNWRhMTQxMCIsImlhdCI6MTY4MDA4NTAyOSwiZXhwIjoxOTk1NDQ1MDI5fQ.lWxAax5wjkAOMbkuu88iK2zAlo58xDW7AJiLzsWChDU"

    urlHomeAssistant = f'{urlHomeAssistant}api/states/{entityID}'  #"http://url/api/states/input_text.value"
    headers = {
        "Authorization": "Bearer " + token,
        "content-type": "application/json",
    }
    response = get(urlHomeAssistant, headers=headers, verify=False)
    data = json.loads(response.text)
    return data['state']

v = getGasPrice()

broker_address = "192.168.1.101"
broker_port = 1883
username = "rpi"
password = "rpimqtt"

client = mqtt.Client()
client.username_pw_set(username, password)
client.connect(broker_address, broker_port)

topic = "Gas_Price"
message = f'{getGasPrice()}'
client.publish(topic, message, retain=True)

client.disconnect()