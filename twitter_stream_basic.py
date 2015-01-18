from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import StreamListener
import time

ckey = "qxkEHQtFppP6zXuRjDBrIDnoz"
csecret = "kffY6ZuqTh9j9du6BHDGcjkxuUC2fYOrxC0dKONskhxyXIdppT"
atoken = "1612285206-XgJ65gHtw2FjA5wQLGLsZx7Ew1EI0sfi5YLoFgF"
atoksec = "D9ZEXZDZs540oBpgnOVSjVYLimvd6bXgzAKzRQBuRF9iK"

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

