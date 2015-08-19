import tweepy
from buddy.keys import (TWITTER_CONS_KEY,
                        TWITTER_SECRET, TWITTER_TOKEN_KEY,
                        TWITTER_TOKEN_SECRET, SITE_URL)

CONSUMER_KEY = TWITTER_CONS_KEY
CONSUMER_SECRET = TWITTER_SECRET
ACCESS_TOKEN_KEY = TWITTER_TOKEN_KEY
ACCESS_TOKEN_SECRET = TWITTER_TOKEN_SECRET




def tweet_status(person, message):
    '''
    updates status of twitter account.
    '''
    
    status = '@' + person +' ' + message
    
    if len(status) > 140:
        raise Exception('status message is too long!')
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    result = api.update_status(status=status)
    
    return result


def conf_tweet(recipient, conf):
    
    message = '''
    ABB: Twitter handle changed.
    Click here to confirm: 
    http://%s/confirm/%s/t/
    '''% (SITE_URL, conf)

    if len(message) > 140:
        raise Exception('status message is too long!')
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.secure = True
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    ##add in a clause here to prevent the rest of API call if
    #the name isnt in the follower list.
    
    
    result = api.send_direct_message(screen_name=recipient, text=message)
    return result

