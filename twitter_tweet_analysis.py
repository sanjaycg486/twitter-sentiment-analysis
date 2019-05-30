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
        pos_rand_var = 0
        neg_rand_var = 0
        total_pos_score = 0
        total_neg_score = 0
        
    
        """ set TwitterSearch parameters"""

        tso.set_keywords([keyword])
        tso.set_language('en')
        tso.set_include_entities(False)

        ts = TwitterSearch(ckey,csecret,atoken,atoksec) #connects to Twitter API 

        for tweet in ts.search_tweets_iterable(tso):

            statement = tweet['text'] #fetches and stores one tweet

            for word in statement.split():
                try: 
                    con = sql.connect('word.db')  #connects to database containing words
                    cur = con.cursor()
                    pos_word = cur.execute("SELECT positive_word from Word where positive_word = ?", (word.lower(),))
                    if pos_word.fetchone()[0] == word:        #if word is in database
                        pos_score +=1
                        
                    else:
                         pos_rand_var = 0
                    con.close()     
                    total_pos_score = pos_rand_var + pos_score 
                except TypeError: #continue if error
                    continue

            for word in statement.split():
                try:
                    con = sql.connect('word.db')  #connects to database containing words
                    cur = con.cursor()
                    neg_word = cur.execute("SELECT negative_word from Word where negative_word = ?", (word.lower(),))
                    if neg_word.fetchone()[0] == word:
                        neg_score -=1
                    else:
                        neg_rand_var = 0
                    con.close()
                    total_neg_score = neg_rand_var + neg_score 
                except TypeError:
                    continue
                


            if total_pos_score == 0 and total_neg_score == 0:
                neutral_count +=1
                print statement, "\n------>Statement is neutral."

            elif total_pos_score>=1 and (total_neg_score==0 or total_neg_score ==-1)  :
                pos_count +=1
                
                print statement, "\n------>Statement is positive."
                
            elif total_pos_score >=0  and (total_neg_score==-2 or total_neg_score ==-3 or total_neg_score<=-5):
                neg_count+=1
                print statement, "\n------>Statement is negative."
            else:
                neutral_count +=1
                print statement, "\n------>Statement is neutral."

                            
            i+=1
            if i == 11: #enter number of tweets you want
                break

        total_tweet = neutral_count+pos_count+neg_count 
        print neutral_count, pos_count, neg_count, total_tweet #prints number of positive, negative, neutral, tweets 

        pos = arange(3)+1
        barh(pos, ( neutral_count, pos_count, neg_count), align = "center", color = '#0099ff')
        yticks(pos,("Neutral Tweets", "Positive Tweets", "Negative Tweets"))
        xlabel("No. of tweets")
        ylabel(keyword.title())
        title("Sentiment Analysis")
        grid(True)
        savefig(keyword.title())

        
        

    except TwitterSearchException as e:
        print "Not connected to internet or error"

search("interstellar")
#search('put your keyword here') #enter keyword 