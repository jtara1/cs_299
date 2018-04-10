import os
import pandas as pd


twitter_user = 'realDonaldTrump'
user_frame = pd.DataFrame(
    pd.read_json('../scrape/twitter_data/{}.json'.format(twitter_user),
                 convert_dates=False,
                 convert_axes=False))

print(user_frame)
print('\n', user_frame.to_json())
