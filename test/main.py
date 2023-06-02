# This is a sample Python script.
import time
from urllib.error import URLError
import paho.mqtt.client as mqtt
import pandas as pd
import time

url = "https://www.omie.es/sites/default/files/dados/NUEVA_SECCION/INT_PBC_EV_H_ACUM.TXT"
# url of the OMIE energy prices for every hour in a year
days = 3  # number of days
lines = days * 24  # number of lines to be read


def getHourValue():
    # Use a breakpoint in the code line below to debug your script.
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
        return D1, D2, P  # if the url was read successfully


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    [Day1, Day2, Price] = getHourValue()  # execute at 3pm ish
    # print(Price)
    # print(Day1)
    # print(Day2)

    broker_address = "192.168.1.101"
    broker_port = 1883
    username = "rpi"
    password = "rpimqtt"

    client = mqtt.Client()
    client.username_pw_set(username, password)
    client.connect(broker_address, broker_port)

    topic = "Energy_Price"
    message = f'{round(Price, 2)}'
    client.publish(topic, message, retain=True)

    client.disconnect()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

from datetime import datetime
import paho.mqtt.client as mqtt
from urllib.error import URLError
from pandas import read_csv

urlOMIE = "https://www.omie.es/sites/default/files/dados/NUEVA_SECCION/INT_PBC_EV_H_ACUM.TXT"
# url of the OMIE energy prices for every hour in a year
days = 30  # number of days
lines = days * 24  # number of lines to be read
BaseValue = 300  # base value (has to be different from 0) is used when the first iteration fails

TimeS = datetime.__new__(datetime, 1, 1, 1, 13, 30, 0)
TimeE = datetime.__new__(datetime, 1, 1, 1, 13, 31, 0)

def getEnergyPrice(OldValue=0):  # returns the mean of energy price (Euro/MWh) of the last "days" days, receive as input the
        #                           last obtained price, if it's the first iteration OldValue should be equal to 0
        try:
            df = read_csv(urlOMIE, skiprows=3, sep=";", encoding="utf-8", header=None, decimal=',', nrows=lines)
            # try to read (days * 24) 720 lines from the given url skipping the first 3 lines, separating the columns on ';'
            # and uses both ',' and '.' as a decimal notation
        except URLError:  # checks if program fails to access the url
            if OldValue == 0:  # if it's the first iteration getValue returns the base value
                return BaseValue
            else:  # else returns the last obtained value
                return OldValue
        else:
            return df[3].mean()  # if the url was read successfully, returns the mean of the price in the last "days" days
        
if __name__ == '__main__':
    v = getEnergyPrice()

    broker_address = "192.168.1.101"
    broker_port = 1883
    username = "rpi"
    password = "rpimqtt"

    client = mqtt.Client()
    client.username_pw_set(username, password)
    client.connect(broker_address, broker_port)

    topic = "Energy_Price"
    message = f'{round(getEnergyPrice(), 2)}'
    client.publish(topic, message, retain=True)

    client.disconnect()