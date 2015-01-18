from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import StreamListener
import time

ckey = "your customer key"
csecret = "your customer key secret"
atoken = "your access token"
atoksec = "your access token secret"

class listener(StreamListener):

    def on_data(self,data):
        try:
            #print data

            tweet = data.split(',"text":"')[1].split('","source')[0]
            print tweet
            return True
        

        except BaseException, e:
            print 'failed,', str(e)
            time.sleep(5)

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,atoksec)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["interstellar"])
