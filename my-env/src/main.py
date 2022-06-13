from mmap import ACCESS_COPY
import check_trades
import os
import tweepy
import time

# CONSTANTS
ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_SECRET')
CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')

print(ACCESS_TOKEN)

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
    media = api.media_upload('images/stock_graph.png')
    api.update_status(status=message, media_ids=[media.media_id])


def check_recent_trade_file():
    recent_trade_file = open('recent_trade.txt', 'r')
    trade = recent_trade_file.readlines()   
    recent_trade_file.close()
    
    return trade


def update_recent_trade_file(trade_dict):
    file = open('recent_trade.txt', 'w')
    file.write(str(trade_dict))
    file.close()
    
    
def format_tweet(trade_dict):
    # reformat the titles to be CEO/Pres/10% etc instead of CEO, Pres, 10%
    title = trade_dict['title']
    title = title.split(', ')
    new_title = ''
    
    for i in range(len(title)):
        new_title += title[i]
        # makes sure the slash isn't printed after the last title
        if i < len(title)-1:
            new_title += '/'
            
    # reformat the insider info from "Last First" to "L. First" to save characters
    insider = trade_dict['insider_name']
    insider = insider.split(' ')
    # adds the last name initial to new_insider
    new_insider = f'{insider[1]} {insider[0][0]}.'
    
    trade_type = ''
    if trade_dict['trade_type'][0] == 'S':
        trade_type = 'sold'
    elif trade_dict['trade_type'][0] == 'B':
        trade_type = 'bought'
    
    num_shares_traded = trade_dict['quantity'].replace('-','')
    
    
    tweet = f"ALERT: {trade_dict['ticker']} {new_title} {new_insider} {trade_type} {num_shares_traded} shares of stock, resulting in an ownership change of {trade_dict['ownership_change_pct']}."
    return tweet


def main():
    api = authenticate_api()
    # every 10 seconds check for a new trade
    while True:
        trade_dict = check_trades.get_trade_info()
        
        # check to see if there trade_dict contains a new trade
        old_trade = check_recent_trade_file()
        update_recent_trade_file(trade_dict)
        new_trade = check_recent_trade_file()
             
        # if there is a new trade, download the graph image and tweet out an alert
        if(old_trade != new_trade):
            check_trades.download_graph(trade_dict)

            tweetMessage = format_tweet(trade_dict)
            send_tweet(tweetMessage, api)

        print(f'formatted: {format_tweet(trade_dict)}')
        
        time.sleep(10)
        

if __name__ == '__main__':
    main()
    