import appdaemon.plugins.hass.hassapi as hass
import time
import datetime
from urllib.error import URLError
import pandas as pd

class energy_price(hass.Hass):
    def initialize(self):
        runtime = datetime.time(0, 0, 0)
        self.run_hourly(self.getHourValue, runtime)
        
        self.energy_price = self.get_entity("sensor.EnergyPrice")
        if not self.energy_price.exists:
            self.energy_price.add(state=123, atributes={"unit_of_measurement": "€/MWh"})
        
        
    def getHourValue(self, kwargs):
        url = "https://www.omie.es/sites/default/files/dados/NUEVA_SECCION/INT_PBC_EV_H_ACUM.TXT"
        # url of the OMIE energy prices for every hour in a year
        days = 3  # number of days
        lines = days * 24  # number of lines to be read
        try:
            df = pd.read_csv(url, skiprows=3, sep=";", encoding="utf-8", header=None, decimal=',', nrows=lines)
            D1 = list(df[3][0:23])
            D2 = list(df[3][24:47])
            D1.insert(0, df[3][47])             # insert the price of hour 24 of the previous day into the 1st position
            D1.insert(24, int(df[0][0][0:2]))   # insert the day into the 25th position
            D2.insert(0, df[3][71])             # insert the price of hour 24 of the previous day into the 1st position
            D2.insert(24, int(df[0][24][0:2]))  # insert the day into the 25th position
            # try to read (days * 24) 72 lines from the given url, skipping the first 3 lines,
            # separating the columns on ';' and uses both ',' and '.' as a decimal notation
            t = time.localtime()
            P = 0
            if D1[24] == t.tm_mday:
                P = D1[t.tm_hour]
            elif D2[24] == t.tm_mday:
                P = D2[t.tm_hour]
        
        except URLError:  # checks if program fails to access the url
            print('Failed to connect\n')
        else:
            self.my_entity = self.get_entity("sensor.EnergyPrice")
            self.my_entity.set_state(state=P)