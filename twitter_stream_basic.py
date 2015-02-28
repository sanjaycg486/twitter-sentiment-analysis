from TwitterSearch import *

ckey = "your customer key"
csecret = "your customer key secret"
atoken = "your access token"
atoksec = "your access token secret"

def search():
            
    try:
        i =1
        keyword = raw_input("Enter the keyword to search: ")

        tso.set_keywords([keyword])
        tso.set_language('en')
        tso.set_include_entities(False)

        ts = TwitterSearch(ckey,csecret,atoken,atoksec)

        
        for tweet in ts.search_tweets_iterable(tso):
            print( i, '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )
            i+=1
            if i == 31:
                break 
        
    except TwitterSearchException as e:
        print (e)
            
search()
