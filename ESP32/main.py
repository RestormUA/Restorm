values = [0, 0, 0]	# array to store values read
current = 0		# 'pointer' to the current position of the array
last = 2		# 'pointer' to the last position used of the array
OldDuty = 0		# Last duty cycle calculated
NewDuty = 0		# Duty Cycle to implement
DeviceP = -1		# Power of the energy accumulator

def sub_cb(topic, msg):
    global values
    global current
    global last
    global OldDuty
    global NewDuty
    global DeviceP
    
    print((topic,msg))
    
    if topic == topic_pwrDif:				# Check if the msg received is the Pp-Pc
        v = -float(msg) if msg != None else -1		# Read Pp-Pc
        if v != values[last]:				# Check if the read value is different from the last one 
            if abs(v - values[last]) >= 100 :		# If the difference from the read and the current is greater
                values = [v, v, v]			# than 100, set the array of values read all equal to the value read
            elif v == 0 :				# If the differnece is equal to 0
                values = [0, 0, 0]			# Set the array of values read equal to 0
            else : 					# 
                values[current] = v			# Insert the value read in the array in the position 'current'
        last = current					# Update 'last' to be equal to 'current'
        current = current + 1 if current < 2 else 0	# Increment 'current' by one, but if circling back to 0 if its greater than 2
        mean = (values[0] + values[1] + values[2]) / 3	# Calculate the mean of the values read
        NewDuty = OldDuty + mean/DeviceP if DeviceP > 100 else OldDuty 	# Calculate the duty cycle
        
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
				###############
duty = 1023
time.sleep(1)			
pwmPin.duty(duty)		# Set the duty cylce to 100% and wait 1s, before and after setting
time.sleep(5)
# # if we go with 2 measures the read msg func returns [Pc,Pp] then we send v as the diff between the 2
while DeviceP == -1:					# Wait until a value is read
   try:
      new_message = client.check_msg()
      DeviceP=client.read_load()			# Read the power of the energy accumulator 
   except OSError as e:
      restart_and_reconnect()
duty = 0
pwmPin.duty(duty)					# Set the duty cycle to 0% and clear the other variables
OldDuty = 0		
NewDuty = 0
values = [0, 0, 0]


ts = time.ticks_ms()					# Get time on which the normal behaviour started, 
							# used to wait 1s before publishing an mqqt msg

while True:
  try:
    new_message = client.check_msg()
    
    duty = 0 if NewDuty*1023<1 else 1023 if NewDuty*1023>1023 else floor(NewDuty*1023)		# Calculate the PWM
    pwmPin.duty(duty)										# Send PWM to IO Port 
    
    if time.ticks_diff(time.ticks_ms(),ts) >= 1000:	# Check it passed 1s from the last time we made a mqtt publish
        ledPin.value(not ledPin.value())		# Change the LED state
        ts = time.ticks_ms()				# Update the time
        client.publish(topic_pub,str(round(duty/10.23,1)))	# Publish the duty cycle
        
    OldDuty = 0 if NewDuty<0 else 1 if NewDuty>1 else NewDuty # Update the Old Duty Cycle to the New Duty Cycle
    
  except OSError as e:
    restart_and_reconnect()
