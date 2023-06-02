#
# Python Script to get a text input from Home Assistant Front-end using REST API
#
from requests import get
import json

#### INPUTS
# Url of the Home Assistant instance
url = "https://paradisepunch.hopto.org:443/"
# Entity ID
entityID = "input_text.value"
# Access token created through Home Assistant profile
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJiMDg2MjVhZjU2MTU0ZmE1YTE2MGIzMjI1NWQ4MjFmYyIsImlhdCI6MTY3MDAxMjY3NiwiZXhwIjoxOTg1MzcyNjc2fQ.wI4fyQbr7gB421_12ihjpO1bI8p_Wj5u2-sX1Fn3CV4"
####

url = url + "api/states/" + entityID  #"https://192.168.1.100:8123/api/states/input_text.value"
headers = {
    "Authorization": "Bearer " + token,
    "content-type": "application/json",
}
response = get(url, headers=headers, verify=True)
data = json.loads(response.text)
print("Entity State: " + data['state'])