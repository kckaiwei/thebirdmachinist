import tweepy, time

from keys import keys

CONSUMER_KEY = keys['CONSUMER_KEY']
CONSUMER_SECRET = keys['CONSUMER_SECRET']
ACCESS_TOKEN = keys['ACCESS_KEY']
ACCESS_TOKEN_SECRET = keys['ACCESS_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

keywords = [
        "rt to", "rt and win", "retweet and win",
    "rt for", "rt 4", "retweet to"
]

bannedwords = [
    "vote","bot"
    ]


def search(twts):
    for i in twts:
        if not any(k in i.text.lower() for k in keywords) or any(k in i.text.lower() for k in bannedwords):
            continue
        # Retweets
        try:
            api.retweet(i.id)
            print "JUST RETWEETED " + (i.text)
        except:
            print "Hm... Something went wrong.\nYou've probably already retweeted this."
        # Follows
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
            api.create_favorite(i.id)
            print "JUST FAVORITED " + (i.text)
        # This part waits a minute before moving onto the next one.
        time.sleep(540)


def run():
    for key in keywords:
        search(api.search(q=key))


run()
