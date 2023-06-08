# Restorm

This is the official repository for all codes being used in Restorm project.


# Folders and Files
## RPI
- *python-scripts*
This codes run in AppDaemon Home Assistant add-on. They should be placed in */config/appdaemon/apps*. 
|File            |Description					|
|----------------|-------------------------------|
|`'energy_price.py'`|Gets the hourly energy price through OMIE database and updates it in the entity sensor.|           
|`'gas_price.py'`|Gets the gas price inputted by the user in the dashboard and updates it in the entity sensor.|

- *configs*

|File            |Description					|
|----------------|-------------------------------|
|`'mqtt-sensor.yaml'`|Configuration for *configuration.yaml* in Home Assistant. Creates sensors for all topics that can be used to store all values.|

## ESP32
All codes are running on Micropython firmware.
|File            |Description					|
|----------------|-------------------------------|
|`'boot.py'`|Runs on boot. Connects to Wifi getting IP via DHCP.|           
|`'main.py'`|Reads current values of Consumed/Generated Power from Shelly's. Calculates Duty-Cycle.|
|`'umqttsimple.py'`|Send Duty-Cycle value to Home Assistant via MQTT.|
