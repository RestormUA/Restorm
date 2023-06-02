# Python code to web scrap the energy price in each hour of the day to calculate the mean in the last 30 days

from urllib.error import URLError
from pandas import read_csv

url = "https://www.omie.es/sites/default/files/dados/NUEVA_SECCION/INT_PBC_EV_H_ACUM.TXT"
# url of the OMIE energy prices for every hour in a year
days = 30  # number of days
lines = days * 24  # number of lines to be read
BaseValue = 300  # base value (has to be different from 0) is used when the first iteration fails


def getValue(OldValue=0):  # returns the mean of energy price (Euro/MWh) of the last "days" days, receive as input the
    #                           last obtained price, if it's the first iteration OldValue should be equal to 0
    try:
        df = read_csv(url, skiprows=3, sep=";", encoding="utf-8", header=None, decimal=',', nrows=lines)
        # try to read (days * 24) 720 lines from the given url skipping the first 3 lines, separating the columns on ';'
        # and uses both ',' and '.' as a decimal notation
    except URLError:  # checks if program fails to access the url
        if OldValue == 0:  # if it's the first iteration getValue returns the base value
            return BaseValue
        else:  # else returns the last obtained value
            return OldValue
    else:
        return df[3].mean()  # if the url was read successfully, returns the mean of the price in the last "days" days
