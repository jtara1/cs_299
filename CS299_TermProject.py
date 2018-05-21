from TwitterAPI import TwitterAPI
import tweepy 
import json

#TWITTER API Credentials 

consumer_key = 'oozwT5VaBKa4bzcT7BdifWOQp'
consumer_secret = '7jU6dWiYy6NHqc8VjTEayleteIL0DZNu8vHt36Kz0GtBDYB9xR'
access_key = "987942030536949761-D9iitIPIUfWkiPiVqfNNyRSvUJ6LHXW"
access_secret = "s5S9tPZKvcYDW56MxGjU53NJ5h3hFkztjn7VNGImuC4w4"



#ask user for screen_name
screen_name=str(input("Please enter a TWITTER User Name:" ))





#initialize tweepy and authorize TWITTER 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)

#create an empty list to add all tweets to
alltweets=[]

#create a reqquest for most recent tweets 
new_tweets = api.user_timeline(screen_name = screen_name,count=100)



alltweets.extend(new_tweets)

outtweets = [[tweet.text.encode("utf-8")] for tweet in alltweets]


print("We are done retrieiving your tweets.\nYou can find them in a file with the"
      +" TWITTER user name you used.")
    
with open(screen_name, 'w') as outfile:
    for tweet in range(len(outtweets)) :
        json.dump(str(outtweets[tweet]), outfile)
