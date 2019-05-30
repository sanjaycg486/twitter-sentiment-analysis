import cgi #The Common Gateway Interface (CGI) is a standard for writing programs that can interact through a Web server with a client running a Web browser.
import html
from TwitterSearch import * #Import twittersearch module
from matplotlib import *    #Import matplotlib module
from time import strftime    #Import time module
from email.utils import parsedate    #Import Miscellaneous utilities
from pylab import *    #Import pylab module
import sqlite3 as sql #import sqlite module

ckey = "Twitter application API key"
csecret = "Twitter application API secret key"
atoken = "Twitter application Access token"
atoksec = "Twitter application Access token secret"

form = cgi.FieldStorage()    #Instantiate only once!
keyword = form.getfirst('q', 'empty')
keyword = html.escape(keyword)
tso = TwitterSearchOrder()    #Create a TwitterSearchOrder object


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
        con = sql.connect('word.db')    #Connects to database containing words
        cur = con.cursor()    
    
        """set TwitterSearch parameters"""

        tso.set_keywords([keyword])    #Set the keyword we are looking for tweets from Twitter
        tso.set_language('en')    #Want to see English tweets only
        tso.set_include_entities(False)    #Don't give us all those entity information

        ts = TwitterSearch(ckey,csecret,atoken,atoksec)    #Connects to Twitter API 

        for tweet in ts.search_tweets_iterable(tso):
            
            tweetDate = parsedate(tweet['created_at'])    #Fetch Tweet Date
            tweetTime = strftime("%H:%M:%S", tweetDate)
            statement = tweet['text']    #Fetch and stores one tweet
            
            print(tweetTime)
			
            for word in statement.split():
                try: 
                    pos_word = cur.execute("SELECT positive_word from Word where positive_word = ?", (word.lower(),))
                    
                    if pos_word.fetchone()[0] == word:    #if word is in database
                        pos_score += 1                        
                    else:
                         pos_rand_var = 0
                             
                    total_pos_score = pos_rand_var + pos_score 
                except TypeError:    #Continue if error
                    continue

            for word in statement.split():
                try:                    
                    neg_word = cur.execute("SELECT negative_word from Word where negative_word = ?", (word.lower(),))
                    
                    if neg_word.fetchone()[0] == word:    #if word is in database
                        neg_score -= 1
                    else:
                        neg_rand_var = 0
                        
                    total_neg_score = neg_rand_var + neg_score 
                except TypeError:    #Continue if error
                    continue               

            if total_pos_score == 0 and total_neg_score == 0:
                neutral_count += 1
                print(statement,'\n------>Statement is neutral.')
            elif total_pos_score >= 1 and (total_neg_score == 0 or total_neg_score == -1):
                pos_count += 1                
                print(statement,'\n------>Statement is positive.')                
            elif total_pos_score >= 0  and (total_neg_score == -2 or total_neg_score == -3 or total_neg_score <= -5):
                neg_count += 1
                print(statement,'\n------>Statement is negative.')
            else:
                neutral_count += 1
                print(statement,'\n------>Statement is neutral.')                            
			
            i += 1
            if i == 50: #Number of tweets you want
                break

        con.close() 
        total_tweet = neutral_count + pos_count + neg_count
         
        print(total_tweet,pos_count,neg_count,neutral_count) #Print Total number of tweets,Positive tweets count,Negative tweets count,Neutral tweets count

        pos = arange(3) + 1        
        
        """Plot bar graph"""
        figure()
        barh(pos, (neutral_count, pos_count, neg_count), align = "center", color = '#0099ff')        
        yticks(pos,("Neu.Tweets", "Pos.Tweets", "Neg.Tweets"))
        xlabel("No. of tweets")
        ylabel(keyword.title())
        title("Sentiment Analysis")
        grid(True) 
        savefig(keyword +" "+ "BarGraph")       
	
        """Plot line graph"""
        figure()
        xlabel(keyword.title())
        ylabel("No. of tweets")        
        title("Sentiment Analysis")
        xticks(pos,("Neu.Tweets", "Pos.Tweets", "Neg.Tweets"))
        plot([1,2,3],[neutral_count, pos_count, neg_count])  
        savefig(keyword +" "+ "LineGraph")    
        show() 
        

    except TwitterSearchException as e:
        print("Not connected to internet or error")

keyword = input("Enter the keyword to search: ")
search(keyword)
