import pandas as pd
import numpy as np
from datetime import datetime
import math
import sklearn
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

pricesDF = pd.read_csv("CryptoPriceData/bitcoin_price.csv")
sentimentDF = pd.read_csv("sentiment_real_scores.csv")
lengthSent = int(len(sentimentDF.index) *.9)

dfX = sentimentDF.iloc[0:lengthSent,:] # dataframe for our training data
trainX = []
dfX2 = sentimentDF.iloc[lengthSent:, :] # dataframe for our testing data, in this case our testing data will literally be one point, so thats a problem
trainY = []

testX = []
testY = []

lm = LinearRegression()
#<<<<<<< HEAD
print (dfX2)
##=======
#>>>>>>> 55a4e38edf44bd71b42e8adeb2cdc5ad1d33d415

for i in range(len(dfX)):
    year =  dfX.iloc[i,0]
    week = dfX.iloc[i,1]
    for j in range(len(pricesDF)):

        if ( pricesDF.iloc[j,(len(pricesDF.columns)-3)] == week and pricesDF.iloc[j,(len(pricesDF.columns)-2)] == year and math.isnan(pricesDF["EndWeekChange"][j]) == False):
            #above if statement just checks to see that for evey year and week in the sentiment scores file, if their is a corresponding year and week point in the price file
            lister = []
            lister.append(dfX["average sentiment score"][i])
            trainX.append(lister)
            lister = []
            trainY.append(pricesDF["EndWeekChange"][j])
i = 0
for ix, x in dfX2["average sentiment score"].iteritems(): # same thing as above but for testing data formation
    year =  dfX2.iloc[i,0]
    week = dfX2.iloc[i,1]
#<<<<<<< HEAD
    print (year)
    print (week)
#=======

#>>>>>>> 55a4e38edf44bd71b42e8adeb2cdc5ad1d33d415
    for j in range(len(pricesDF)):
        if ( pricesDF.iloc[j,(len(pricesDF.columns)-3)] == week and pricesDF.iloc[j,(len(pricesDF.columns)-2)] == year and math.isnan(pricesDF["EndWeekChange"][j]) == False):
            #continue
            testX.append(dfX2["average sentiment score"][ix])
            testY.append(pricesDF["EndWeekChange"][j])
    i+=1
#<<<<<<< HEAD
print (trainX)
model = lm.fit(trainX,trainY)
print (model.coef_)
#=======

model = lm.fit(trainX,trainY)
print "model COEF"
print model.coef_ # there is only a .4% correlation LMAOOOO. Prob because we have really spotty data and not much of it, but at least that is something to show
print r2_score(trainY,model.predict(trainX))
#>>>>>>> 55a4e38edf44bd71b42e8adeb2cdc5ad1d33d415

#graph
plt.scatter(trainX,trainY)
plt.ylabel("weekly change in price % ")
plt.xlabel("sentiment score of tweets")
plt.plot(trainX, model.predict(trainX))
plt.show()
