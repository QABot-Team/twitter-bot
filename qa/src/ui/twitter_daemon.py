from tweepy import OAuthHandler, API, Stream
from ui.twitter_listener import TwitterListener
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, USER_ID
from utils.logger import Logger


def start_daemon():
    """ Authenticate to twitter api and start a listener """

    # Authentication by OAuth
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.secure = True
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # connect to api to reply to tweets
    api = API(auth)

    # own StreamListener Implementation
    listener = TwitterListener(api)

    # init and start TwitterListener to get tweet updates
    stream = Stream(auth, listener)
    Logger.info("Start Twitter Daemon...")
    stream.filter(follow=[str(USER_ID)])
