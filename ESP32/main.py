values = [0, 0, 0]
current = 0
last = 2
OldDuty = 0
NewDuty = 0
DeviceP = -1

def sub_cb(topic, msg):
    global values
    global current
    global last
    global OldDuty
    global NewDuty
    global DeviceP
    
    print((topic,msg))
    
    if topic == topic_pwrDif:
        v = -float(msg) if msg != None else -1
        if v != values[last]:
            if abs(v - values[last]) >= 100 :
                values = [v, v, v]
            elif v == 0 :
                values = [0, 0, 0]
            else : 
                values[current] = v
        last = current
        current = current + 1 if current < 2 else 0
        mean = (values[0] + values[1] + values[2]) / 3
        NewDuty = OldDuty + mean/DeviceP if DeviceP > 100 else OldDuty 
        
def connect_and_subscribe():
  global client_id, mqtt_server, topic_pwrLd , topic_pwrDif
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_pwrLd)
  client.subscribe(topic_pwrDif)
  print('Connected to %s MQTT broker, subscribed to %s topic and %s topic' % (mqtt_server, topic_pwrLd, topic_pwrDif))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

duty = 1023
time.sleep(1)
pwmPin.duty(duty)
# # if we go with 2 measures the read msg func returns [Pc,Pp] then we send v as the diff between the 2
while DeviceP == -1:
   try:
      new_message = client.check_msg()
      DeviceP=client.read_load()
   except OSError as e:
      restart_and_reconnect()
# DeviceP = 1000
duty = 0
pwmPin.duty(duty)
OldDuty = 0
NewDuty = 0
values = [0, 0, 0]


ts = time.ticks_ms()

while True:
  try:
    new_message = client.check_msg()
    
    duty = 0 if NewDuty*1023<1 else 1023 if NewDuty*1023>1023 else floor(NewDuty*1023)
    pwmPin.duty(duty)
    
    if time.ticks_diff(time.ticks_ms(),ts) >= 1000:
        ledPin.value(not ledPin.value())
        ts = time.ticks_ms()
        client.publish(topic_pub,str(round(duty/10.23,1)))
        client.publish(topic_pubV,str(values)+' '+str(client.read_pwr())+' '+str(DeviceP)+' '+str(NewDuty)+' '+str(duty))
        
    OldDuty = 0 if NewDuty<0 else 1 if NewDuty>1 else NewDuty
    
  except OSError as e:
    restart_and_reconnect()