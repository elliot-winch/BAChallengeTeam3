import os
import csv
import tweepy
from textblob import TextBlob
from datetime import datetime

#Twitter API credentials
consumer_key = "FJWOzGHGKB71vVWaARRJs43Sp"
consumer_secret = "aRRk3Ms49NqpQEbDz4a5GN0pMjc1YaJ14OFtOojBWJpBNPvRHu"
access_key = "923721999108763648-Mg4cL4qtvLcGuzovcWeA1NtMLTQ5NSX"
access_secret = "Fc4LYOdF7kzpkU9d4JYgdkNgzCTs9vks8uSL6EIlMvmWb"


class TweetSemanticAnalyser():
    def __init__(self, username, filtered = False):
        self.filterWords = ["bitcoin", "cryptocurrency", "crypto", "ico"]
        self.filtered = False
        self.username = username
        self.alltweets = []
        self.semanticScores = {}
        self.getAllUserTweets(username)

    #Courtesy of yanofsky (https://gist.github.com/yanofsky/tweet_dumper.py"
    def getAllUserTweets(self, createFile=True):
        #Twitter only allows access to a users most recent 3240 tweets with this method

        try:
            with open(username + "_tweets.csv", "r") as f:
                print(username + " tweets found")
                csvreader = csv.reader(f, delimiter = ",")
                for row in csvreader:
                    try:
                        datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")

                        self.semanticScores[row[1]] = TextBlob(row[2]).sentiment
                    except IndexError:
                        continue
                    except ValueError:
                        continue

        except:
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
                print ("getting tweets for %s" % (self.username))

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

            if(self.filtered == False):
                for tweet in self.alltweets:
                    self.semanticScores[tweet.created_at] = TextBlob(tweet.text).sentiment
            else:
                for tweet in self.alltweets:
                    tweetByWords = tweet.text.split()


                    for word in tweetByWords:
                        for filterWord in self.filterWords:
                            if(word == filterWord):
                                self.semanticScores[tweet.created_at] = TextBlob(tweet.text).sentiment
                                break
                            else:
                                continue
                            break

    def getSentimentScores(self):
        return self.semanticScores

if __name__ == "__main__":

    filtered = {} #dictionary to map username to bool, whether or not to filter

    with open("Twitter Users.csv", 'r') as csvFile:
        csvreader = csv.reader(csvFile, delimiter = ",")

        for row in csvreader:
            if(row[3] == 'F'): # place U here if you want the unfiltered ones 
                filtered[row[0][1:]] = row[3] == 'U'

    #usernames = ["coindesk", "Cointelegraph"]
    #filteredUsernames = []

    values = {}
    numTweetsInWeek = {}

    for username in filtered:
        try:
            a = TweetSemanticAnalyser(username, filtered[username])
        except tweepy.TweepError as e:
            print (e.message[0]['code'])  # prints 34
            print (e.args[0][0]['code'])  # prints 34

        scores = a.getSentimentScores()

        for date in scores:
            if type(date) is str:
                datetimeObj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            else:
                datetimeObj = date

            weekString = str(datetimeObj.year)

            if datetimeObj.isocalendar()[1] < 10 :
                weekString += '0'

            weekString+= str(datetimeObj.isocalendar()[1])

            if(weekString in values):
                values[weekString] += scores[date][0]
                numTweetsInWeek[weekString] +=1
            else:
                values[weekString] = scores[date][0]
                numTweetsInWeek[weekString] = 1

    outtweets = [[date[:4], date[-2:], values[date] / numTweetsInWeek[date]] for date in values]
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    with open(os.path.join(location, 'sentiment_biased_scores.csv'), 'w+') as f: # where sentiment real scores is the unbiased file
        writer = csv.writer(f)
        writer.writerow(["year","week","average sentiment score"])
        writer.writerows(outtweets)
