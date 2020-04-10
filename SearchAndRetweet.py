import tweepy
from new_api import create_api

# Create API object
api = create_api()


limit = 0

for tweet in api.search(q="'Cyber security' OR 'hack' OR 'hacking' OR 'Network security' OR 'Cybercrime'", lang="en", rpp=8, result_type="popular"):
    if tweet.in_reply_to_status_id is not None or tweet.user.id == api.me():
        # This tweet is a reply or I'm its author so, ignore it
        continue
    if not tweet.retweeted:
        try:
            tweet.retweet()
            limit += 1
        except Exception as e:
            print("Error on fav and retweet")
    if limit > 5 :
        break