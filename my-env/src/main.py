from mmap import ACCESS_COPY
import check_trades
import os
import tweepy
import time

# test commit 1
# CONSTANTS
ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_SECRET')
CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')

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
    media = api.media_upload('my-env/images/stock_graph.png') # get the stock graph image
    api.update_status(status = message, media_ids = [media.media_id]) # tweet the message with the image attached

# reply to the most recent tweet from the account
def send_reply(message, api):
    tweet = api.user_timeline(user_id=1483177923427409924, count=1)[0] # get the most recent tweet
    api.update_status(status = message, in_reply_to_status_id = tweet.id , auto_populate_reply_metadata=True) # send the reply
    print('reply should sent')

# returns the details of the trade in the recent_trade file. used to see if the most recent is different, meaning
# a new trade has been made  
def check_recent_trade_file():
    recent_trade_file = open('recent_trade.txt', 'r')
    trade = recent_trade_file.readlines()   
    recent_trade_file.close()
    
    return trade

# overwrites the recent_trade file with the newest trade
def update_recent_trade_file(trade_dict):
    file = open('recent_trade.txt', 'w')
    file.write(str(trade_dict))
    file.close()
    
# takes the info from the trade_dict dictionary and turns it into a more readable format for the tweet
def format_tweet(trade_dict):
    # reformat the titles to be CEO/Pres/10% etc instead of CEO, Pres, 10%D
    title = trade_dict['title']
    title = title.split(', ')
    new_title = ''
    
    for i in range(len(title)):
        new_title += title[i]
        if i < len(title)-1: # makes sure the slash isn't printed after the last title
            new_title += '/'
            
    # reformat the insider info from "Last First" to "First L." to save characters
    insider = trade_dict['insider_name']
    insider = insider.split(' ')
    new_insider = f'{insider[1]} {insider[0][0]}.'
    
    # when looking at stock trades, "+500" is converted to "bought 500" to make report more readable
    trade_type = ''
    if trade_dict['trade_type'][0] == 'S':
        trade_type = 'sold'
        num_shares_traded = trade_dict['quantity'].replace('-','')
    elif trade_dict['trade_type'][0] == 'P':
        trade_type = 'bought'
        num_shares_traded = trade_dict['quantity'].replace('+','')
    
    tweet = f"ALERT: {trade_dict['ticker']} {new_title} {new_insider} {trade_type} {num_shares_traded} shares of stock, resulting in an ownership change of {trade_dict['ownership_change_pct']}."
    return tweet

# replies to the main tweet with additional information about the trade
def format_reply(trade_dict):
    value = trade_dict['value'].replace('-', '')
    reply = f"MORE INFO:\nCompany Name: {trade_dict['company_name']}\nFiling Date/Time: {trade_dict['filing_date']}\nPrice of Stock: {trade_dict['price']}\nValue of Transaction: {value}"
    return reply


def main():
    api = authenticate_api()
    # every 10 seconds check for a new trade
    while True:
        trade_dict = check_trades.get_trade_info() # gets the most recent trade listed on OpenInsider
        
        # check to see if there trade_dict contains a new trade
        old_trade = check_recent_trade_file()
        update_recent_trade_file(trade_dict)
        new_trade = check_recent_trade_file()
             
        if(old_trade != new_trade): # if there is a new trade, download the graph image and tweet out an alert
            check_trades.download_graph(trade_dict) # downloads image of stock graph

            tweetMessage = format_tweet(trade_dict)
            replyMessage = format_reply(trade_dict)
            
            send_tweet(tweetMessage, api) # sends main tweet
            send_reply(replyMessage, api) # replies to the main tweet with more info

        print(f'formatted: {format_tweet(trade_dict)}')
        
        time.sleep(10)
        

if __name__ == '__main__':
    main()
    