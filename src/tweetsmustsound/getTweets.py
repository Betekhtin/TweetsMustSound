import twitter
import tweets/secrets
import re

class TwitMiner:
	####################################################initialize twitter api
	def __init__(self):
		self.api = 	twitter.Api(consumer_key = secrets.consumer_key,
				  consumer_secret = secrets.consumer_secret,
				  access_token_key = secrets.access_token_key,
				  access_token_secret = secrets.access_token_secret)

####################################################clean tweet from urls and not letters
	def clean_tweet(self, tweet):
		text = re.sub(r"^https?:\/\/.*[\r\n]*", '', tweet, flags=re.MULTILINE)
		return ' '.join(re.sub("(@[A-Za-z]+)|([^A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

####################################################get hash tags from tweet
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

####################################################get tweets from user
	def get_tweets(self, username):

		numofload = 20 #total numbers of target tweets
		numofhashedtweets = 50 #numbers of searched tweets by hashes

		#####initial search
		statuses = self.api.GetSearch(raw_query = "q=from%3A" + username + "&lang=en&count=" + str(numofload))
		iterations = min(statuses[0].user.statuses_count // numofload, 16)
		statuses = [s for s in statuses if '#' in s.text]

		######iterate over max allowed tweets to get w\o exceeding rate
		for i in range(0,iterations):
			lastId = statuses[-1].id
			#search on iteration
			newstatuses = self.api.GetSearch(raw_query = "q=from%3A" + username + "&max_id=" + str(lastId) + "&lang=en&count=" + str(numofload))
			newstatuses_hashed = [s for s in newstatuses if '#' in s.text]
			#calc last iteration with respect to total numbers of target tweets
			if len(newstatuses_hashed) + len(statuses) > numofload:
				ind = 0, numofload - len(statuses)
				for k in sorted(ind, reverse=True):
					del newstatuses_hashed[k]
				del newstatuses_hashed[-1]
			#fill result search and check total number of target tweets
			statuses += newstatuses_hashed
			if len(statuses)>=numofload:
				break

		#get tweet text from tweet obj
		statuses_text = [(s.text) for s in statuses]
		#get hashes from tweet text
		st_hashes = [self.get_hashes(s) for s in statuses_text]

		statuses_text = [self.clean_tweet(s.text) for s in statuses]

		hash_stat =[]
		#get tweets by hashes for every tweet
		for h in st_hashes:
			for i in h:
				t=[]
				if len(i)>0:
					it_data = self.api.GetSearch(raw_query = "q=twitter%20" + i + "&lang=en&count=" + str(numofhashedtweets))
					t = [self.clean_tweet(s.text) for s in it_data]
				hash_stat.append(t)
		###################### return target tweets and tweets searched by hashes 
		return statuses_text, hash_stat

uname = "jayzclassicbars"

gtw = TwitMiner()
tw,htw = gtw.get_tweets(uname)
