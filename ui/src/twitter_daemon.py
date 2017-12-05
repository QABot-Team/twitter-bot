from tweepy import OAuthHandler, API, Stream
from twitter_listener import TwitterListener
from config import consumer_key, consumer_secret, access_token, access_token_secret, own_user_id


def start_daemon():
    """ Authenticate to twitter api and start a listener """

    # Authentication by OAuth
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)

    # connect to api to reply to tweets
    api = API(auth)

    # own StreamListener Implementation
    listener = TwitterListener(api)

    # init and start TwitterListener to get tweet updates
    stream = Stream(auth, listener)
    stream.filter(follow=[str(own_user_id)])
