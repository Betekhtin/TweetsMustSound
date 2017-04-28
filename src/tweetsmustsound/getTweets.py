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
		statuses = self.api.GetSearch(raw_query = "q=from%3A" + username + "&lang=en&count=220")
		#statuses = self.api.GetUserTimeline(screen_name = username, count = 200)
		iterations = min(statuses[0].user.statuses_count // 202, 16)
		statuses = [s for s in statuses if '#' in s.text]
		print([(s.text) for s in statuses if '#' in s.text])
		for i in range(0,iterations):
			lastId = statuses[-1].id
			nst = self.api.GetSearch(raw_query = "q=from%3A" + username + "&max_id="+str(lastId)+"&lang=en&count=220")
			q = [s for s in nst if '#' in s.text]
			statuses += q
			if len(statuses)>=20:
				break
		statuses_text = [(s.text) for s in statuses]
		st_hashes = [self.get_hashes(s) for s in statuses_text]
		statuses_text = [self.clean_tweet(s.text) for s in statuses]
		hash_stat =[]
		for h in st_hashes:
			for i in h:
				t=[]
				if len(i)>0:
					it_data = self.api.GetSearch(raw_query = "q=twitter%20 +" + i + "&lang=en&count=20")
					t = [self.clean_tweet(s.text) for s in it_data]
				hash_stat.append(t)
		return statuses_text, hash_stat

	def eng_tweets(self, statuses):
		result = []
		for status in statuses:
			if status.lang == "en":
				result.append(status)
		return result

uname = "jayzclassicbars"

gtw = TwitMiner()
tw,htw = gtw.get_tweets(uname)
print(tw)
print(htw)

