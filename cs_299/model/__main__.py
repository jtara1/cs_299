from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import re
from pprint import pprint
import time
import json
from glob import glob
import os
from os.path import basename, dirname, abspath, join
import pandas as pd
from collections import Counter, OrderedDict
from functools import reduce
from multiprocessing import Pool

from cs_299.scrape.__main__ import download_tweets

stop_words = stopwords.words('english')


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
        self.filtered_words = stop_words + [
            'https',
        ]
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

    def create_frame_from_tweets(self, tweets_file_path):
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

        for tweet_id in tweets:
            # remove whitespace characters and put each word in a list
            words = word_tokenize(tweets[tweet_id]['body'])

            # make each word lowercase
            words = [word.lower() for word in words]

            # filter out insignificant words & words that aren't all
            # alphabetical characters
            words = list(
                filter(
                    lambda word:
                        word not in self.filtered_words and word.isalpha(),
                    words))

            tweets[tweet_id]['body'] = words
            tweets[tweet_id]['word_count'] = Counter(words)

        user_frame = pd.DataFrame(tweets)
        return twitter_user, user_frame


class TweetQuery(TweetProcessor):
    def __init__(self, tweets_file_path='./scrape/twitter_data'):
        """Builds upon the TweetProcessor to provide methods to
        query the data

        :param tweets_file_path:
        """
        super(TweetQuery, self).__init__(tweets_file_path)
        self.create_frames()

    def get_most_frequent_words(self, twitter_user, limit=10):
        twitter_user = twitter_user.lower()

        try:
            series = self.user_frames[twitter_user].loc['word_count']
        except KeyError:
            path = download_tweets(twitter_user, self.tweets_file_path)
            user, frame = self.create_frame_from_tweets(path)
            self.user_frames[user] = frame
            return self.get_most_frequent_words(twitter_user, limit)

        word_count = reduce(lambda x, y: x + y, series.values)
        return OrderedDict(word_count.most_common(limit))


if __name__ == '__main__':
    # automatically loads tweet data and transforms into pd.DataFrame
    tp = TweetQuery()
    top_10_words = tp.get_most_frequent_words('realDonaldTrump')
    print(top_10_words)
    # pprint(tp.user_frames)
