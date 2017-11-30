import os
import csv
import tweepy

#Twitter API credentials
consumer_key = "FJWOzGHGKB71vVWaARRJs43Sp"
consumer_secret = "aRRk3Ms49NqpQEbDz4a5GN0pMjc1YaJ14OFtOojBWJpBNPvRHu"
access_key = "923721999108763648-Mg4cL4qtvLcGuzovcWeA1NtMLTQ5NSX"
access_secret = "Fc4LYOdF7kzpkU9d4JYgdkNgzCTs9vks8uSL6EIlMvmWb"


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print ("getting tweets before %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print ("...%s tweets downloaded so far" % (len(alltweets)))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
	
	location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

	#write the csv	
	with open(os.path.join(location, '%s_tweets.csv' % screen_name), 'w+') as f:
            writer = csv.writer(f)
            writer.writerow(["id","created_at","text"])
            writer.writerows(outtweets)
	
	pass


if __name__ == '__main__':
	#pass in the username of the account you want to download
    get_all_tweets("J_tsar")