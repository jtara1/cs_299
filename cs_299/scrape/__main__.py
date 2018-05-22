import tweepy
import json
from cs_299.twitter_api_keys import *
import os
from os.path import join, dirname, basename


def download_tweets(screen_name, output_directory='twitter_data'):
    #initialize tweepy and authorize TWITTER
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    api = tweepy.API(auth)

    #create an empty list to add all tweets to
    alltweets = []

    #create a reqquest for most recent tweets
    new_tweets = api.user_timeline(screen_name=screen_name, count=100)

    alltweets.extend(new_tweets)

    outtweets = [
        {
            "body": tweet.text.decode('utf-8') if isinstance(tweet.text, bytes)
            else tweet.text
        }
        for tweet in alltweets
    ]

    with open(join(output_directory, '{}.json'.format(screen_name.lower())), 'w') as outfile:
        json.dump(outtweets, outfile)


if __name__ == '__main__':
    download_tweets('realdonaldtrump')