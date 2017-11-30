from textblob import TextBlob
from TweetCollector import UserTweetCollector

def calculateSemanticScore(userTweets):
    semanticScore = []
    
    for tweet in userTweets:
        tweetText = tweet.text.encode("utf-8")
        semanticScore.append(TextBlob(tweetText).sentiment)
        
    return semanticScore
    
if __name__ == "__main__":
    collector = UserTweetCollector()
    listy = collector.get_all_tweets("J_tsar")
    print(len(listy))
    #print(calculateSemanticScore())