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
	def get_hashes(self, tweet_text):
		hashes = [s for s in tweet_text.split() if (s[0]=='#')]
		nhashes=[]
		for shash in hashes:
			nhash=[]
			for ch in shash:
				if(ch=='#'):
					nhash+="%23"
				else:
					nhash+=self.clean_tweet(ch)
			nhashes.append(''.join(nhash))
		return nhashes

	def get_tweets(self, username):
		statuses = api.GetUserTimeline(screen_name = username, count = 200)
		statuses_text = [(s.text) for s in statuses]
		hashes = [self.get_hashes(s) for s in statuses_text]
		statuses_text = [self.clean_tweet(s.text) for s in statuses]
		statuses_by_hashes = api.GetSearch(query_row = "q=")
		return statuses_text;

uname = "realDonaldTrump"
api = twitter.Api(consumer_key = secrets.consumer_key,
				  consumer_secret = secrets.consumer_secret,
				  access_token_key = secrets.access_token_key,
				  access_token_secret = secrets.access_token_secret)
t = api.GetSearch("q=%23nasa")
print(len(t))	
#gtw = TwitMiner
#tw = gtw.get_tweets(gtw,uname)
#for i in tw:
#	print(gtw.get_hashes(gtw,i))
