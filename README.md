# Restorm

This is the official repository for all codes being used in Restorm project.


# Folders and Files
## RPI
- \>*/python-scripts*

This codes run in AppDaemon Home Assistant add-on. They should be placed in */config/appdaemon/apps*. 

|File            |Description					|
|----------------|-------------------------------|
|`'energy_price.py'`|Gets the hourly energy price through OMIE database and updates it in the entity sensor.|           
|`'gas_price.py'`|Gets the gas price inputted by the user in the dashboard and updates it in the entity sensor.|

- \>*/configs*

This files are essential to run previous codes and create entities/automation.

|File            |Description					|
|----------------|-------------------------------|
|`'apps.yaml'`|Configuration to run the previous python-scripts in the AppDaemon add-on. Should be placed in */config/appdaemon/apps/apps.yaml* inside Home Assistant.|
|`'appdaemon.yaml'`|Configuration for AppDaemon add-on. Needs Home Assistant IP and a long lived token created by the user. Should be placed in */config/appdaemon/appdaemon.yaml* inside Home Assistant.|
|`'configuration.yaml'`|Example configuration of our Home Assistant. Creates a MQTT sensor for Duty-Cycle (PWM_Sensor) and configurates InfluxDB add-on. Should be placed in */config/configuration.yaml* inside Home Assistant.|

- \>*/automation*

Code for our automation that sends which mode should the ESP32 work on.

|File            |Description					|
|----------------|-------------------------------|
|`'MQTTMode.yaml'`|Automation to send mode (Sell/Buy) to ESP32 via MQTT based on the user selection.|

## ESP32
All codes are running on Micropython firmware.

|File            |Description					|
|----------------|-------------------------------|
|`'boot.py'`|Runs on boot. Connects to Wifi getting IP via DHCP.|           
|`'main.py'`|Reads current values of Consumed/Generated Power from Shelly's. Calculates Duty-Cycle.|
|`'umqttsimple.py'`|Send Duty-Cycle value to Home Assistant via MQTT.|
