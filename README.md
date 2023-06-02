# Restorm

This is the official repository for all codes being used in Restorm project.


# Folders and Files
## RPI
- *python-scripts*

|File            |Description					|
|----------------|-------------------------------|
|`'energy_price.py'`|Gets the hourly energy price through OMIE and sends the value to a Home Assistant sensor via MQTT.|           
|`'gas_price.py'`|Gets the gas price inputted by the user in the dashboard using the Home Assistant API and sends the value to a sensor via MQTT.|
|`'store_prices.py'`|Gets current gas and energy prices in Home Assistant and stores them in a file called `'prices.json'`.|
|`'mode.py'`|Gets both values from `'prices.json'` and calculates the which mode should be used (if energy should be selled or bought).|

This codes run periodically using *crontab*.
- *configs*

|File            |Description					|
|----------------|-------------------------------|
|`'crontab-code'`|Configuration for *crontab*. Timers can be seen bellow.|           
|`'mqtt-sensor.yaml'`|Configuration for *configuration.yaml* in Home Assistant. Creates sensors for all topics that can be used to store all values.|

> *crontab-code* 
> 
> `'energy_price.py'` - runs one time every hour
> 
> `'gas-price.py'` - runs one time every 5 minutes
> 
> `'store-prices.py'` - runs one time every 10 minutes
> 
> `'mode.py'` - runs one time every 1 minute
> 

## ESP32
All codes are running on Micropython firmware.
|File            |Description					|
|----------------|-------------------------------|
|`'boot.py'`|Runs on boot. Connects to Wifi getting IP via DHCP.|           
|`'main.py'`|Reads current values of Consumed/Generated Power from Shelly's. Calculates Duty-Cycle.|
|`'umqttsimple.py'`|Send Duty-Cycle value to Home Assistant via MQTT.|
