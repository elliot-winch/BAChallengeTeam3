import pandas as pd
import numpy as np
from datetime import datetime


df = pd.read_csv("CryptoPriceData/inputbitcoinprices.csv")
weeknoList = []
yearnoList = []
month = 0

for val in df["Date"]:
    abrev =  val[0:3]
    if abrev == "Jan":
        month = 1
    if abrev == "Feb":
        month = 2
    if abrev == "Mar":
        month = 3
    if abrev == "Apr":
        month = 4
    if abrev == "May":
        month = 5
    if abrev == "Jun":
        month = 6
    if abrev == "Jul":
        month = 7
    if abrev == "Aug":
        month = 8
    if abrev == "Sep":
        month = 9
    if abrev == "Oct":
        month = 10
    if abrev == "Nov":
        month = 11
    if abrev == "Dec":
        month = 12

    date = int(val[4:6])

    year = int(val[8:12])
    s = "20120213"
    date = datetime(year= year, month= month, day= date)
    weekNumber = datetime.date(date).isocalendar()[1]

    weeknoList.append(weekNumber)
    yearnoList.append(year)
df["Week Number"] = weeknoList
df["Year"] = yearnoList
df = df.iloc[:,1:] # removing extra first column index

df["EndWeekChange"] = [None] * len(df)
oldstart = 40 # initial week in price data set
initialIndex = 0
for i in range(len(df)):
    newstart = df.iloc[i, 7]
    print newstart
    if(newstart != oldstart):
        oldPrice  = df["Close"][initialIndex]
        newPrice = df["Close"][i]
        df.iloc[initialIndex, (len(df.columns)-1)] = ((oldPrice-newPrice)/newPrice) * 100 # where i know its weird but old price is actually the most recent price, new price is just further down the time series so its actually an older date 
        initialIndex = i
    oldstart = newstart
df.to_csv("CryptoPriceData/bitcoin_price.csv")
