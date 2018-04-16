from pprint import pprint
import time
import json
from glob import glob
import os
from os.path import basename, dirname, abspath, join
import pandas as pd
from collections import Counter
from multiprocessing import Pool


class TweetProcessor:
    def __init__(self, tweets_file_path='../scrape/twitter_data'):
        """Transforms a tweets in the form of JSON to be contained in a
        pandas.DataFrame

        :param tweets_file_path: directory containing JSON files \n
            where each file is named after a twitter user and the \n
            contents should follow the schema: \n
            { 123: {"body": "tweet text here"}} where 123 is the id \n
            of the tweet
        """

        self.tweets_file_path = abspath(tweets_file_path)
        self.user_frames = {}

    def create_frames(self, processes=4):
        """Create a frame from the data from each JSON file found in
        self.tweets_file_path and use multiprocessing transform the
        data from the file into a pandas.DataFrame

        :param processes: the number of processes to use in the Pool \n
            that processes each file in parallel
        :return:
        """
        mp_pool = Pool(processes)
        list_of_files = glob(join(self.tweets_file_path, '*.json'))

        # make a dictionary out of the list of tuples where the first
        # value in each tuple is the twitter_user & 2nd is the frame
        self.user_frames = dict(
            mp_pool.map(
                self.create_frame_from_tweets,
                list_of_files))

    @staticmethod
    def create_frame_from_tweets(tweets_file_path):
        """Transform tweet data on a specific user and file into a
        pandas.DataFrame

        :param tweets_file_path:
        :rtype: tuple
        :return: tuple containing twitter user (str) and the frame \n
            (pandas.DataFrame)
        """
        twitter_user = basename(tweets_file_path).split('.json')[0]

        with open(tweets_file_path, 'r') as f:
            tweets = json.load(f)

        # TODO: use regex to split by /s
        # TODO: filter out insignificant words (the, a, there, be ...)
        for tweet_id in tweets:
            tweets[tweet_id]['body'] = tweets[tweet_id]['body'].split(' ')
            tweets[tweet_id]['word_count'] = Counter(tweets[tweet_id]['body'])

        user_frame = pd.DataFrame(tweets)
        # print(user_frame)
        return twitter_user, user_frame

    def serialize(self, file_path='user_frames.json'):
        json_data = {
            twitter_user: frame.to_json()
            for twitter_user, frame in self.user_frames.items()
        }
        print()

        with open(file_path, 'w') as f:
            json.dump(f, json_data)

    def deserialize(self, file_path='user_frames.json'):
        with open(file_path, 'r') as f:
            json_data = json.load(f)

        self.user_frames = {
            twitter_user: frame.from_dict()
            for twitter_user, frame in json_data.items()
        }
        

class Query:
    def __init__(self, user_frames):
        pass

if __name__ == '__main__':
    tp = TweetProcessor()
    tp.create_frames()
    # pprint(tp.user_frames)
    tp.serialize()
