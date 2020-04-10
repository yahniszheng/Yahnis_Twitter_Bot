import tweepy
import threading
from new_api import create_api

#Global parameter
TWEETS_UPDATE_INTERVAL=36000 # 10 hours
FOLLOWERS_UPDATE_INTERVAL=300 # 10 minutes

class TwitterManager:

    def __init__(self,periodic = False, keywords = "'Cyber security' OR 'hack' OR 'hacking' OR 'Cybercrime'", text= r"Check this out, generated by a twitter bot #COMP6441", num = 5, limit = 3):
        self.api = create_api()
        self.keywords = keywords
        self.num = num
        self.limit = limit
        self.text = text
        self.periodic = periodic

    def update_tweets_with_tag(self, periodic = False):
        i = 0
        for tweet in self.api.search(q=self.keywords, lang="en", count = self.num, rpp=self.num, result_type="popular"):
            if tweet.in_reply_to_status_id is not None or tweet.user.id == self.api.me():
                # This tweet is a reply or I'm its author so, ignore it
                continue

            if not tweet.retweeted:
                try:
                    tid = tweet.id
                    self.api.update_status(self.text, attachment_url = "https://twitter.com/Mastercard/status/" + str(tid))
                    i += 1
                except tweepy.TweepError as e:
                    print(e.reason)

            if not tweet.favorited:
                # Mark it as Liked, since we have not done it yet
                try:
                    tweet.favorite()
                except Exception as e:
                    print("Error on fav")

            if i > self.limit :
                break
                
        if self.periodic :
            threading.Timer(TWEETS_UPDATE_INTERVAL, self.update_tweets_with_tag).start()

    def follow_followers(self, periodic = False):
        for follower in tweepy.Cursor(self.api.followers).items():
            if not follower.following:
                print(f"Following {follower.name}")
                follower.follow()
        
        if self.periodic :
            threading.Timer(FOLLOWERS_UPDATE_INTERVAL, self.follow_followers).start()
    
    def update_tweets_without_tag(self, periodic = False):
        i = 0
        for tweet in self.api.search(q=self.keywords, lang="en", count = self.num, rpp=self.num, result_type="popular"):
            if tweet.in_reply_to_status_id is not None or tweet.user.id == self.api.me():
                # This tweet is a reply or I'm its author so, ignore it
                continue

            if not tweet.retweeted:
                try:
                    tweet.retweet()
                    i += 1
                except Exception:
                    print("Error on fav and retweet")

            if i > self.limit :
                break
        
        if self.periodic :
            threading.Timer(TWEETS_UPDATE_INTERVAL, self.update_tweets_without_tag).start()

    def run_in_period(self):
        update_tweets_thread = threading.Thread(target=self.update_tweets_with_tag, daemon=True)
        follow_follower_thread = threading.Thread(target=self.follow_followers, daemon=True)
        update_tweets_thread.start()
        follow_follower_thread.start()


if __name__ == "__main__":
    m = TwitterManager(num=5, limit = 2, periodic = True)
    m.run_in_period()