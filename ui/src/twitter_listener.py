from tweepy.streaming import StreamListener
import json

own_user_id = 833302096413937664


class TwitterListener(StreamListener):
    def __init__(self, twitter_api):
        self.api = twitter_api
        super(StreamListener, self).__init__()

    def on_data(self, data):
        """ gets triggered by a new tweet """
        # print(data)
        json_obj = json.loads(data)
        user_name = json_obj.get('user').get('screen_name')
        user_id = json_obj.get('user').get('id')

        # check if the tweet was initiated by another user or by the twitter bot
        if user_id != own_user_id:
            tweet_id = json_obj.get('id')
            self.api.update_status('@' + user_name + ' Automatic Tweepy Answer!', tweet_id)
        return True

    def on_error(self, status):
        """ get triggered if an error occurs """
        print(status)
