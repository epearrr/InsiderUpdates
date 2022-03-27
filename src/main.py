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
    status = api.update_status(status=message)


def update_recent_trade_file(trade_dict):
    file = open('src/recent_trade.txt', 'w')
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
    while True:
        
        trade_dict = check_trades.get_trade_info()
        
        recent_trade_file = open('src/recent_trade.txt', 'r')
        old_trade = recent_trade_file.readlines()   
        recent_trade_file.close()
        
        update_recent_trade_file(trade_dict)
        
        recent_trade_file = open('src/recent_trade.txt', 'r')
        new_trade = recent_trade_file.readlines()   
        recent_trade_file.close()
        
        print(f'Equal? {old_trade == new_trade}')
        
        if(old_trade != new_trade):
            tweetMessage = format_tweet(trade_dict)
            send_tweet(tweetMessage, api)

        print(f'formatted: {format_tweet(trade_dict)}')

        
        time.sleep(10)
        

if __name__ == '__main__':
    main()