import os
import csv
import tweepy
from textblob import TextBlob


#Twitter API credentials
consumer_key = "FJWOzGHGKB71vVWaARRJs43Sp"
consumer_secret = "aRRk3Ms49NqpQEbDz4a5GN0pMjc1YaJ14OFtOojBWJpBNPvRHu"
access_key = "923721999108763648-Mg4cL4qtvLcGuzovcWeA1NtMLTQ5NSX"
access_secret = "Fc4LYOdF7kzpkU9d4JYgdkNgzCTs9vks8uSL6EIlMvmWb"


class TweetSemanticAnalyser():
    def __init__(self, username):
        self.username = username
        self.alltweets = []
        self.semanticScores = {}
        self.getAllUserTweets(username)

    #Courtesy of yanofsky (https://gist.github.com/yanofsky/tweet_dumper.py"
    def getAllUserTweets(self, createFile=True):
        #Twitter only allows access to a users most recent 3240 tweets with this method

        #authorize twitter, initialize tweepy
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)

        #make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(self.username,count=200)

        #save most recent tweets
        self.alltweets.extend(new_tweets)

        if(len(self.alltweets) <= 0):
            print("Failed to find tweets")
            return

        #save the id of the oldest tweet less one
        oldest = self.alltweets[-1].id - 1

        #keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            print ("getting tweets before %s" % (oldest))

            #all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(screen_name = self.username,count=200,max_id=oldest)

            #save most recent tweets
            self.alltweets.extend(new_tweets)

            #update the id of the oldest tweet less one
            oldest = self.alltweets[-1].id - 1
            print ("...%s tweets downloaded so far" % (len(self.alltweets)))

        #transform the tweepy tweets into a 2D array that will populate the csv
        outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in self.alltweets]
        location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

        if(createFile):
            with open(os.path.join(location, '%s_tweets.csv' % self.username), 'w+') as f:
                writer = csv.writer(f)
                writer.writerow(["id","created_at","text"])
                writer.writerows(outtweets)

        for tweet in self.alltweets:
            self.semanticScores[tweet.created_at] = TextBlob(tweet.text).sentiment


    def getSentimentScores(self):
        return self.semanticScores

if __name__ == "__main__":

    usernames = ["coindesk", "Cointelegraph"]

    values = {}
    numTweetsInWeek = {}

    for username in usernames:
        try:
            a = TweetSemanticAnalyser(username)
        except tweepy.TweepError as e:
            print (e.message[0]['code'])  # prints 34
            print (e.args[0][0]['code'])  # prints 34

        scores = a.getSentimentScores()

        for date in scores:

            weekString = str(date.year)

            if date.isocalendar()[1] < 10 :
                weekString += '0'

            weekString+= str(date.isocalendar()[1])

            if(weekString in values):
                values[weekString] += scores[date][0]
                numTweetsInWeek[weekString] +=1
            else:
                values[weekString] = scores[date][0]
                numTweetsInWeek[weekString] = 1

    outtweets = [[date[:4], date[-2:], values[date] / numTweetsInWeek[date] for date in values]
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    with open(os.path.join(location, 'sentiment scores.csv'), 'w+') as f:
                writer = csv.writer(f)
                writer.writerow(["week","year","sentiment"])
                writer.writerows(outtweets)
