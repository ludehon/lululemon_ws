import json, tweepy


class TwitterClient:
    def __init__(self, creds_path):
        f = open(creds_path)
        credentials = json.load(f)
        f.close()
        self.auth = tweepy.OAuth1UserHandler(
            credentials["consummer_key"], credentials["consummer_secret"],
            credentials["access_token"], credentials["access_token_secret"]
        )
        self.api = tweepy.API(self.auth)
    
    def tweet(self, message):
        self.api.update_status(message)
