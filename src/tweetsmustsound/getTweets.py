import twitter
import secrets
import re

class TwitMiner:
	def __init__(self):
		self.api = 	twitter.Api(consumer_key = secrets.consumer_key,
				  consumer_secret = secrets.consumer_secret,
				  access_token_key = secrets.access_token_key,
				  access_token_secret = secrets.access_token_secret)

	def clean_tweet(self, tweet):
		text = re.sub(r"^https?:\/\/.*[\r\n]*", '', tweet, flags=re.MULTILINE)
		return ' '.join(re.sub("(@[A-Za-z]+)|([^A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

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
		statuses = self.api.GetUserTimeline(screen_name = username, count = 200)
		
		#iterations = min(tweets[0].user.statuses_count // 200, 16)

		#for i in range(0,iterations):
		#	lastId = tweets[-1].id
		#	statuses += api.GetUserTimeline(screen_name = screen_name, 
		#							  	  count = 200, 
		#						  	      max_id = lastId)
		
		statuses_text = [(s.text) for s in statuses]
		#hashes = list(filter(None,[self.get_hashes(s) for s in statuses_text]))
		st_hashes = [self.get_hashes(s) for s in statuses_text]
		statuses_text = [self.clean_tweet(s.text) for s in statuses]
		hash_stat =[]
		for h in st_hashes:
			t=[]
			for i in h:
				if len(i)>0:
					it_data = self.api.GetSearch(raw_query = "q=twitter%20&count=20&" + i)
					t = [self.clean_tweet(s.text) for s in it_data]
			hash_stat.append(t)
		return statuses_text,hash_stat
	def eng_tweets(self, statuses):
		result = []
		for status in statuses:
			if status.lang == "en":
				result.append(status)
		return result

uname = "realDonaldTrump"
gtw = TwitMiner()
tw,htw = gtw.get_tweets(uname)
