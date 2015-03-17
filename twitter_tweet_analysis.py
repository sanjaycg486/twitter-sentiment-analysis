from TwitterSearch import * #import twittersearch module

tso = TwitterSearchOrder()

ckey = "your customer key"
csecret = "your customer key secret"
atoken = "your access token"
atoksec = "your access token secret"


import sqlite3 as sql #import sqlite module
con = sql.connect('word.db')  #connects to database containing words
cur = con.cursor()


def search(keyword):
            
    try:
        i = 1
        pos_score = 0
        neg_score = 0
        neutral_count = 0
        pos_count = 0
        neg_count = 0
    
""" set TwitterSearch parameters"""

        tso.set_keywords([keyword])
        tso.set_language('en')
        tso.set_include_entities(False)

        ts = TwitterSearch(ckey,csecret,atoken,atoksec) #connects to Twitter API 

        for tweet in ts.search_tweets_iterable(tso):

            statement = tweet['text'] #fetches and stores one tweet

            for word in statement.split():
                try: 
                    pos_word = cur.execute("SELECT positive_word from Word where positive_word = ?", (word.lower(),))
                    if pos_word.fetchone()[0] == word:        #if word is in database
                        pos_score +=1
                    except TypeError: #continue if error
                    continue

            for word in statement.split():
                try:
                    neg_word = cur.execute("SELECT negative_word from Word where negative_word = ?", (word.lower(),))
                    if neg_word.fetchone()[0] == word:
                        neg_score -=1
                except TypeError:
                    continue



            if pos_score == 0 and neg_score == 0:
                neutral_count +=1
                print statement, "\n------>Statement is neutral."

            elif pos_score>=1 and neg_score==0:
                pos_count +=1
                print statement, "\n------>Statement is positive."
                
            elif pos_score>=1 and (neg_score==-1 or neg_score ==-3):
                neg_count+=1
                print statement, "\n------>Statement is negative."
                
            elif neg_score !=0 and neg_score%2 == 0:
                pos_count +=1
                print statement, "\n------>statement is positive."
                        
            i+=1
            if i == 11: #enter number of tweets you want
                break

        total_tweet = neutral_count+pos_count+neg_count 
        print neutral_count, pos_count, neg_count, total_tweet #prints number of positive, negative, neutral, tweets            
        

    except TwitterSearchException as e:
        print "Not connected to internet or error"

search('put your keyword here') #enter keyword 
