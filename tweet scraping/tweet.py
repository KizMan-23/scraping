from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint


MINIMUM_TWEETS = 30  #increase the number of min tweets
QUERY = 'bitcoin' #use X Advanced Search for complex or more specific queries

## login credentials
config = ConfigParser()
config.read('config.ini')
username = config['X']['username']
password = config['X']['password']
email = config['X']['email']

# create csv file
with open("bitcoin_tweets.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow('Tweet_count', 'Username', 'Text', 'Created At', 'Retweets', 'Likes')

# authenticate to X.com
#1) Use login credentials 2) use cookies
client = Client(language='en-US')
#client.login(auth_info_1 = username, auth_info_2 = email, password= password)
#client.save_cookies('cookies.json')

client.load_cookies('cookies.json')

def get_tweets(tweets): 
    if tweets is None:
        print(f'{datetime.now()} - Getting tweets..')
        #get tweets
        tweets = client.search_tweet(QUERY, product='Latest')
    else:
        wait_time = randint(5,10)
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds')
        time.sleep(wait_time)
        tweets = tweets.next()
    return tweets

tweet_count = 0
tweets = None

while tweet_count < MINIMUM_TWEETS:
    try:
        tweets = get_tweets(tweets)
    except TooManyRequests as e:   #To allow for time rest when rate limit is hit
        rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
        print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
        wait_time = rate_limit_reset - datetime.now()
        time.sleep(wait_time.total_seconds())

    if not tweets:
        print(f'{datetime.now()} - No more tweets')
        break

    for tweet in tweets:
        tweet_count += 1
        tweet_data = [tweet_count, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favourite_count]
        with open('bitcoin_tweets.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(tweet_data)


print(f'{datetime.now()} - Done got {tweet_counts} tweets found')