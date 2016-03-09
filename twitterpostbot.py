import tweepy, time, os, re, pdb

from keys import keys

CONSUMER_KEY = keys['CONSUMER_KEY']
CONSUMER_SECRET = keys['CONSUMER_SECRET']
ACCESS_TOKEN = keys['ACCESS_KEY']
ACCESS_TOKEN_SECRET = keys['ACCESS_SECRET']


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit = True)

keywords = [
        "rt to win", "rt and win", "retweet and win",
    "rt for", "rt 4", "retweet to win"
]

bannedwords = [
    "vote","bot","bieber"
    ]

running = True

def search(twts):
    failure = 0
    tweeted = False
    if not os.path.isfile("tweets_replied.txt"):
        tweets_replied = []
    else:
        with open("tweets_replied.txt" , "r") as f:
            tweets_replied = f.read()
            tweets_replied = tweets_replied.split("\n")
            tweets_replied = filter(None, tweets_replied)
    for i in twts:
        if not any(k in i.text.lower() for k in keywords) or any(k in i.text.lower() for k in bannedwords):
            continue
        # Retweets
        if str(i.id) not in tweets_replied:
            tweets_replied.append(i.id)
            print "Appended"
            try:
                api.retweet(i.id)
                print "JUST RETWEETED " + (i.text)
                tweeted = True
                if "follow" in i.text or "Follow" in i.text or "FOLLOW" in i.text:
                # This part follows the actual contest-holder, instead of some random person who retweeted their contest
                    tweet = i.text
                    if tweet[0:3] == "RT ":
                        tweet = tweet[3:]
                    if tweet[0] == "@":
                        splittext = (tweet).split(":")
                        username = str(splittext[0]).replace("@", "")
                        api.create_friendship(username)
                        print "JUST FOLLOWED " + (username)
                    else:
                        username = i.user.screen_name
                        api.create_friendship(username)
                        print "JUST FOLLOWED " + str(username)

                    # This next part favorites tweets if it has to
                    if "fav" in i.text or "Fav" in i.text or "FAV" in i.text:
                        try: 
                            api.create_favorite(i.id)
                            print "JUST FAVORITED " + (i.text)
                        except:
                            print "Must have already favorited!"
            # Tweet Failed
            except:
                failure = failure + 1
                print "Hm... Something went wrong.\nYou've probably already retweeted this."

            with open("tweets_replied.txt" , "w") as f:
                for tweet in tweets_replied:
                    f.write(str(tweet) + "\n")
            # Sleeps only if Tweet is successful
            if failure == 10:
                time.sleep(120)
                failure = 0
            if tweeted == True:
                print "Sleeping"
                time.sleep(480)
            tweeted = False



def run():
    for key in keywords:
        search(api.search(q=key))

while 1==1:
    run()
