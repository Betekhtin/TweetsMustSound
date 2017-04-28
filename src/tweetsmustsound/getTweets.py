import twitter
import secrets

api = twitter.Api(consumer_key = apiKeys.consumer_key,
				  consumer_secret = apiKeys.consumer_secret,
				  access_token_key = apiKeys.access_token_key,
				  access_token_secret = apiKeys.access_token_secret)

users = api.GetFriends()

#auth = tweepy.OAuthHandler(apiKeys.consumer_key, apiKeys.consumer_secret)
#auth.set_access_token(apiKeys.access_token_key, apiKeys.access_token_secret)

#api = tweepy.API(auth)
#public_tweets = api.home_timeline()
#for tweet in public_tweets:
#    print (tweet.text)