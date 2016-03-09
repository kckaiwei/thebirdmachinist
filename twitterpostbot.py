import tweepy, time

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
    tweeted = False
    for i in twts:
        if not any(k in i.text.lower() for k in keywords) or any(k in i.text.lower() for k in bannedwords):
            continue
        # Retweets
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
            print "Hm... Something went wrong.\nYou've probably already retweeted this."
        # Sleeps only if Tweet is successful
       
        if tweeted == True:
            print "Sleeping"
            time.sleep(480)
        tweeted = False


def run():
    for key in keywords:
        search(api.search(q=key))

while 1==1:
    run()
