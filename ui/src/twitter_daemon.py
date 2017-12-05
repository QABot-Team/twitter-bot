from tweepy import OAuthHandler, API, Stream
from twitter_listener import TwitterListener

consumer_key = "eYgDDJoYaNowTPZInYfwtwrVu"
consumer_secret = "eTEsZlXKXNcEpZ0BpCVOYSwtyBJqxKBCa5WA9DTYv1FGzXxCQR"

access_token = "833302096413937664-srib3XFTjgURkG9G4YYpxC2LEyBiuQL"
access_token_secret = "m1yI2LIIjk2Mn7dgSsYBm4UeocrU0D9k0sL7E8gq9DQsw"


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
    stream.filter(follow=['833302096413937664'])
