import json
import tweepy

f = open("credentials.json")
credentials = json.load(f)
f.close()

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(
   credentials["consummer_key"], credentials["consummer_secret"],
   credentials["access_token"], credentials["access_token_secret"]
)


# Create API object
api = tweepy.API(auth)
print(api.verify_credentials().screen_name)

# Create a tweet
api.update_status("Hello Tweepy")