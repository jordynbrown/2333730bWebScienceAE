import pymongo
from pymongo import MongoClient as Connection
import json
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import datetime
import unittest
import sys

#WebScienceAE - 2333730b

# This information sets up the connection information for Mongodb
# In this case, the database is called 'webScience'
# The collected is called Coronavirus
connection = Connection('localhost', 27017)
db = connection.webScience
db.Coronavirus.create_index("id", unique=True, dropDups=True)
collection = db.Coronavirus

# This list stores the keywords which will be searched for in the live tweets
# In this case the word 'Coronavirus' and the hashtag '#Coronavirus' will both be collected
keywords = ['Coronavirus', '#Coronavirus'] 

# Only allows tweets in English to be collected
language = ['en']

# The keys connect to my Twitter app which is used to stream data
# These have been left blank as per instructions
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

# This will collect live Tweets from the stream and store the chosen fields into my Coronavirus collection, webScience database
class StdOutListener(StreamListener):

    def on_data(self, data):

        # Load the Tweet into the variable "t"
        t = json.loads(data)
        
        try:
            # Select the data from the tweet and store it in the Coronavirus collection
            tweet_id = t['id_str']  # The Tweet ID as a string
            username = t['user']['screen_name']  # Username of the current user tweeting
            followers = t['user']['followers_count']  # The number of followers the Tweet author has
            text = t['text']  # All text tweeted by the user
            hashtags = t['entities']['hashtags']  # Hashtags included in the tweet
            dt = t['created_at']  # Timestamp of creation as a string
            language = t['lang']  # Language used - should filter only English tweets

            # Convert the timestamp string given by Twitter to a date object called "created" which is more easily readable
            created = datetime.datetime.strptime(dt, '%a %b %d %H:%M:%S +0000 %Y')


            # Load all of the extracted data (above) into the variable "tweet" that will be stored into the webScience
            tweet = {'id':tweet_id, 'username':username, 'followers':followers, 'text':text, 'hashtags':hashtags, 'language':language, 'created':created}

            # Save to the webScience database
            collection.save(tweet)

            # Optional - Print the username and text of each Tweet to your console as they are pulled from the stream
            # I used this to first test that data was coming in, then to keep track of the number of tweets collected
            print (username + ':' + ' ' + text)
            return True
        except:
            print(t)


    # Used for debugging, prints error to the console if needed
    def on_error(self, status):
        print(status)

     

# Tweepy code - Uses variables at the top of the script
if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=keywords, languages=language, is_async=True)