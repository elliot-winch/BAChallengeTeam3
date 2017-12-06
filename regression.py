import pandas as pd
import numpy as np
from datetime import datetime
import math
import sklearn
from sklearn.linear_model import LinearRegression

pricesDF = pd.read_csv("CryptoPriceData/bitcoin_price.csv")
sentimentDF = pd.read_csv("sentiment_scores.csv")
lengthSent = int(len(sentimentDF.index) *.8)

dfX = sentimentDF.iloc[0:lengthSent,:]
trainX = []
dfX2 = sentimentDF.iloc[lengthSent:, :]
trainY = []

testX = []
testY = []

lm = LinearRegression()
print (dfX2)

for i in range(len(dfX)):
    year =  dfX.iloc[i,0]
    week = dfX.iloc[i,1]
    for j in range(len(pricesDF)):

        if ( pricesDF.iloc[j,(len(pricesDF.columns)-3)] == week and pricesDF.iloc[j,(len(pricesDF.columns)-2)] == year and math.isnan(pricesDF["EndWeekChange"][j]) == False):
            #continue
            lister = []
            lister.append(dfX["sentiment"][i])
            trainX.append(lister)
            lister = []
            trainY.append(pricesDF["EndWeekChange"][j])
i = 0
for ix, x in dfX2["sentiment"].iteritems():
    year =  dfX2.iloc[i,0]
    week = dfX2.iloc[i,1]
    print (year)
    print (week)
    for j in range(len(pricesDF)):
        if ( pricesDF.iloc[j,(len(pricesDF.columns)-3)] == week and pricesDF.iloc[j,(len(pricesDF.columns)-2)] == year and math.isnan(pricesDF["EndWeekChange"][j]) == False):
            #continue
            testX.append(dfX2["sentiment"][ix])
            testY.append(pricesDF["EndWeekChange"][j])
    i+=1
print (trainX)
model = lm.fit(trainX,trainY)
print (model.coef_)

    #print "*********************"
