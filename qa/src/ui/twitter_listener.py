from tweepy.streaming import StreamListener
from qa_process_impl import process_answer_question
from utils.logger import Logger
from config import MAX_ANSWER_LENGTH_TWITTER, USER_ID, USER_NAME
import json


class TwitterListener(StreamListener):
    def __init__(self, twitter_api):
        self.api = twitter_api
        super(StreamListener, self).__init__()

    def on_data(self, data):
        """ gets triggered by a new tweet """
        tweet_json = json.loads(data)
        user_name = tweet_json.get('user').get('screen_name')
        user_id = tweet_json.get('user').get('id')

        # check if the tweet was initiated by another user or by the twitter bot
        if user_id != USER_ID:
            Logger.info("New Tweet received: " + str(tweet_json.get('text')))

            tweet_id = tweet_json.get('id')
            question = tweet_json.get('text')
            question = question.replace(USER_NAME, '')
            answer = process_answer_question(question)

            reply_text = '@' + user_name + ' The answer is: ' + answer

            # cut after MAX_ANSWER_LENGTH_TWITTER chars
            reply_text = reply_text[:MAX_ANSWER_LENGTH_TWITTER]

            self.api.update_status(reply_text, tweet_id)

    def on_error(self, status):
        """ get triggered if an error occurs """
        print(status)
