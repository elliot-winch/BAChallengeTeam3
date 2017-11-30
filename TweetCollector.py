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
        self.alltweets = []
        self.semanticScores = {}
    
    #Courtesy of yanofsky (https://gist.github.com/yanofsky/tweet_dumper.py"
    def getAllUserTweets(self, screen_name, createFile=True):
        #Twitter only allows access to a users most recent 3240 tweets with this method
        
        #authorize twitter, initialize tweepy
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)
                
        #make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name = screen_name,count=200)
        
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
            new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
            
            #save most recent tweets
            self.alltweets.extend(new_tweets)
            
            #update the id of the oldest tweet less one
            oldest = self.alltweets[-1].id - 1
            print ("...%s tweets downloaded so far" % (len(self.alltweets)))
            
        #transform the tweepy tweets into a 2D array that will populate the csv	
        outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in self.alltweets]
        location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        
        if(createFile):
            with open(os.path.join(location, '%s_tweets.csv' % screen_name), 'w+') as f:
                writer = csv.writer(f)
                writer.writerow(["id","created_at","text"])
                writer.writerows(outtweets) 
            
    def analyseTweets(self):
        for tweet in self.alltweets:
            self.semanticScores[tweet.created_at] = TextBlob(tweet.text).sentiment
            
    def getSentimentScores(self):
        return self.semanticScores
            
if __name__ == "__main__":
    a = TweetSemanticAnalyser()
    a.getAllUserTweets("J_tsar")
    a.analyseTweets()
    print(a.getSentimentScores())
    