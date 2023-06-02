import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
from math import floor
esp.osdebug(None)
import gc
gc.collect()

freq = 5000

ledPin = machine.Pin(2, machine.Pin.OUT)
pwmPin = machine.PWM(machine.Pin(5),freq)

ssid = "network_ID"		# 'REPLACE_WITH_YOUR_SSID'
password = "password"		# 'REPLACE_WITH_YOUR_PASSWORD'
mqtt_server = '192.168.1.101'	# 'REPLACE_WITH_YOUR_MQTT_BROKER_IP'
#user pass mqttesp32
#EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())
topic_pwrDif = b'shellies/shellyem-C45BBE788077/emeter/0/power'
topic_pwrLd = b'shellies/shellyem-C45BBE788077/emeter/1/power'
topic_pub = b'esp32/duty-cycle'
topic_pubV = b'esp32/values'


station = network.WLAN(network.STA_IF)

station.active(True)
#station.ifconfig(('192.168.1.51','255.255.255.0','192.168.1.1'))
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())
