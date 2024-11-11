from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint


MINIMUM_TWEETS = 20
QUERY = 'bitcoin'

## login credentials
config = ConfigParser()
config.read('config.ini')
username = config['X']['username']
password = config['X']['password']
email = config['X']['email']

# authenticate to X.com
#1) Use login credentials 2) use cookies
client = Client(language='en-US')
#client.login(auth_info_1 = username, auth_info_2 = email, password= password)
#client.save_cookies('cookies.json')

client.load_cookies('cookies.json')

#get tweets
tweets = client.search_tweet(QUERY, product='Latest')

print(tweets)


for tweet in tweets:
    print(vars(tweet))
    break