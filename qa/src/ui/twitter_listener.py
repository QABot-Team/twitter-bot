from tweepy.streaming import StreamListener
from qa_process_impl import process_answer_question
from ui.config import own_user_name, own_user_id
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
        if user_id != own_user_id:
            print("====================================\n")
            print("New Tweet received:\n" + str(tweet_json.get('text')) + "\n")

            tweet_id = tweet_json.get('id')
            question = tweet_json.get('text')
            question = question.replace(own_user_name, '')
            answer = process_answer_question(question)

            print("The answer is:\n" + answer + "\n")

            reply_text = '@' + user_name + ' The answer is: ' + answer
            self.api.update_status(reply_text, tweet_id)

    def on_error(self, status):
        """ get triggered if an error occurs """
        print(status)
