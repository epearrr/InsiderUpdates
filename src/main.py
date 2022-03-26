import env_variables
import check_trades
import os
import tweepy
import time

# CONSTANTS
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')

# authenticate API keys and return API object
def authenticate_api():
    twitter_auth_keys = {
        "consumer_key"        : CONSUMER_KEY,
        "consumer_secret"     : CONSUMER_SECRET,
        "access_token"        : ACCESS_TOKEN,
        "access_token_secret" : ACCESS_SECRET
    }

    auth = tweepy.OAuthHandler(
            twitter_auth_keys['consumer_key'],
            twitter_auth_keys['consumer_secret']
            )
    auth.set_access_token(
            twitter_auth_keys['access_token'],
            twitter_auth_keys['access_token_secret']
            )
    api = tweepy.API(auth)
    return api

# send a tweet
def send_tweet(message, api):
    status = api.update_status(status=message)


def update_recent_trade_file(trade_dict):
    file = open('pythonVer/src/recent_trade.txt', 'w')
    file.write(str(trade_dict))
    file.close()
    
    
def format_tweet(trade_dict):
    # reformat the titles to be CEO/Pres/10% etc instead of CEO, Pres, 10%
    title = trade_dict['title']
    title = title.split(', ')
    
    # if the length of the split is greater than 1, add the slashes
    if len(title) > 1:
        newTitle = ''
        
        for i in range(len(title)):
            newTitle += title[i]
            newTitle += '/'
            
    else:
        newTitle = title
        
    tweet = f"{trade_dict['ticker']} {newTitle}"
    
    return tweet


def main():
    api = authenticate_api()
    while True:
        
        trade_dict = check_trades.get_trade_info()
        
        recent_trade_file = open('pythonVer/src/recent_trade.txt', 'r')
        old_trade = recent_trade_file.readlines()   
        recent_trade_file.close()
        
        update_recent_trade_file(trade_dict)
        
        recent_trade_file = open('pythonVer/src/recent_trade.txt', 'r')
        new_trade = recent_trade_file.readlines()   
        recent_trade_file.close()
        
        print(f'Equal? {old_trade == new_trade}')
        
        if(old_trade != new_trade):
            tweetMessage = format_tweet(trade_dict)
            send_tweet(tweetMessage, api)
        else:
            print(f'formatted: {format_tweet(trade_dict)}')

        
        time.sleep(10)
        

if __name__ == '__main__':
    main()