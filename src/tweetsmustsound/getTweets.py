import twitter
import secrets
import re

api = twitter.Api(consumer_key = secrets.consumer_key,
				  consumer_secret = secrets.consumer_secret,
				  access_token_key = secrets.access_token_key,
				  access_token_secret = secrets.access_token_secret)


class TwitMiner:
	def __init__(self):
		self.api = 	twitter.Api(consumer_key = secrets.consumer_key,
				  consumer_secret = secrets.consumer_secret,
				  access_token_key = secrets.access_token_key,
				  access_token_secret = secrets.access_token_secret)
	def clean_tweet(tweet):
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
	def get_hashes(tweet_text):
		hashes = [s for s in tweet_text.split() if (s[0]=='#')]
	def get_tweets(self, username):
		statuses = api.GetUserTimeline(screen_name = username)
		statuses_text = [self.clean_tweet(s.text) for s in statuses]
		return statuses_text;

uname = "realDonaldTrump"
gtw = TwitMiner
tw = gtw.get_tweets(gtw,uname)
print(tw)