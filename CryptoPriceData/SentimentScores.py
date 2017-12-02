import os
import csv
import tweepy
from textblob import TextBlob
from TweetCollector import TweetSemanticAnalyser


if __name__ == "__main__":
    
    usernames = ["J_tsar", "bachallengeteam3"]
    
    values = {}
    
    for username in usernames:
        a = TweetSemanticAnalyser(username)
        
        for tweetSentiment in a.getSentimentScores():
            print(tweetSentiment)
        
    