import twitter
import secrets
import re

api = twitter.Api(consumer_key = secrets.consumer_key,
				  consumer_secret = secrets.consumer_secret,
				  access_token_key = secrets.access_token_key,
				  access_token_secret = secrets.access_token_secret)

def clean_tweet(tweet):
	return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_tweets(screen_name):
	tweets = api.GetUserTimeline(screen_name = screen_name, count = 200)

#	for i in range(0,16):
#		lastId = tweets[-1].id
#		tweets += api.GetUserTimeline(screen_name = screen_name, 
#									  count = 200, 
#								  max_id = lastId)
	return tweets

def print_tweets(tweets):
	i = 0
	for tweet in tweets:
		print(str(i) + ":" + tweet.text)
		i += 1

tweets = get_tweets("AsWhichOneIAm")
print_tweets(tweets)