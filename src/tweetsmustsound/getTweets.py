import twitter
import secrets
import re

class TwitMiner:
####################################################initialize twitter api
	def __init__(self):
		self.api = twitter.Api(consumer_key = secrets.consumer_key,
				  consumer_secret = secrets.consumer_secret,
				  access_token_key = secrets.access_token_key,
				  access_token_secret = secrets.access_token_secret)

####################################################clean tweet from urls and not letters
	def clean_tweet(self, tweet):
		text = re.sub(r"^https?:\/\/.*[\r\n]*", '', tweet, flags=re.MULTILINE)
		return ' '.join(re.sub("(@[A-Za-z]+)|([^A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

####################################################get tweets from user
	def get_tweets(self, username):

		numofload = 5 #total numbers of target tweets
		numofhashedtweets = 50 #numbers of searched tweets by hashes
		numberofRT = 5 #number of retweets in searched by hashes 
		numofInitialLoad = 20 #number of initial load with respect to needs in finding 1 hashed tweet
		#####initial search
		statuses = self.api.GetSearch(raw_query = "q=from%3A" + username + "&lang=en&count=" + str(numofInitialLoad))		
		iterations = min(statuses[0].user.statuses_count // numofload, 16)
		statuses = [s for s in statuses if '#' in s.text]
		if len(statuses) > numofload:
			ind = 0, numofload - len(statuses)
			for k in sorted(ind, reverse = True):
				del statuses[k]
			del statuses[-1]
			######iterate over max allowed tweets to get w\o exceeding rate
		else:
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
		statuses_text = [self.clean_tweet(s.text) for s in statuses]
		
		#get hashes from tweet text
		st_hashes = [["%23" + shashtags_single.text for shashtags_single in s.hashtags] for s in statuses]

		hash_stat =[]
		#get tweets by hashes for every tweet
		for h in st_hashes:
			curr_numRT = 0
			for i in h:
				t=[]
				if len(i)>0:
					it_data = self.api.GetSearch(raw_query = "q=twitter%20" + i + "&lang=en&count=" + str(numofhashedtweets))
					####control number of retweeted tweets by one hash
					for s in it_data:
						if curr_numRT < numberofRT:
							if s.text[0:2] == "RT":
								curr_numRT = curr_numRT + 1				
							t.append(self.clean_tweet(s.text))
						else:
							if s.text[0:2] == "RT":
								continue
							else:
								curr_numRT = 0
				hash_stat.append(t)
		###################### return target tweets and tweets searched by hashes 
		return statuses_text, hash_stat

uname = "realDonaldTrump"

gtw = TwitMiner()
tw,htw = gtw.get_tweets(uname)
for i in htw:
	print(i)