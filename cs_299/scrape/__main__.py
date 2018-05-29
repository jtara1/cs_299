import tweepy
import json
from cs_299.twitter_api_keys import *
import os
from os.path import join, dirname, basename
import pathlib


def download_tweets(screen_name, output_directory='twitter_data'):
    """Download recent tweets given a twitter username. Saved
    in the output_directory which is relative to this file

    :param screen_name: username of twitter user
    :param output_directory: will contain the json file contain \n
        data on tweets
    :return: file path the serialized tweets
    """
    #initialize tweepy and authorize TWITTER
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    api = tweepy.API(auth)

    #create an empty list to add all tweets to
    alltweets = []

    #create a reqquest for most recent tweets
    new_tweets = api.user_timeline(screen_name=screen_name, count=100)

    alltweets.extend(new_tweets)

    outtweets = {
        tweet.id:
        {
            "body": tweet.text.decode('utf-8') if isinstance(tweet.text, bytes)
            else tweet.text
        }
        for tweet in alltweets
    }

    # take the name of the directory and save it relative to this file
    output_directory = join(dirname(__file__), basename(output_directory))

    file_path = join(output_directory, '{}.json'.format(screen_name.lower()))

    # combines $ mkdir -p /my/path/
    # $ touch /my/path/file.json
    pathlib.Path(dirname(file_path)).mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w') as outfile:
        json.dump(outtweets, outfile)

    return file_path


if __name__ == '__main__':
    # test
    download_tweets('realDonaldTrump')
