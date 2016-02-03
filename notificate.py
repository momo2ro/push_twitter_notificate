from pushbullet import Pushbullet
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy.streaming import StreamListener
import json

pushbullet_access_token     = ""

twitter_consumer_key        = ""
twitter_consumer_secret     = ""
twitter_access_token        = ""
twitter_access_token_secret = ""


pusher = Pushbullet(pushbullet_access_token)
auth = OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
auth.set_twitter_access_token(twitter_access_token, twitter_access_token_secret)
api = API(auth)
me = api.me()


class TwitterEventListener(StreamListener):
    def on_data(self, data):
        jdata = json.loads(data)
        try:
            if jdata.get("event") == "favorite" and jdata["source"]["id"] != me.id:
                title = "@{screen_name}からふぁぼられました".format(**jdata["source"])
                body  = jdata["target_object"]["text"]
                pusher.push_note(title, body)
            elif jdata.get("event") == "unfavorite" and jdata["source"]["id"] != me.id:
                title = "@{screen_name}からあんふぁぼされました".format(**jdata["source"])
                body  = jdata["target_object"]["text"]
                pusher.push_note(title, body)
            elif jdata.get("event") == "follow":
                title = "@{screen_name}からフォローされました".format(**jdata["source"])
                pusher.push_note(title, "")
            elif "retweeted_status" in jdata and jdata["retweeted_status"]["user"]["id"] == me.id:
                title = "@{screen_name}からRTされました".format(**jdata["user"])
                body  = jdata["retweeted_status"]["text"]
                pusher.push_note(title, body)
            elif "in_reply_to_user_id" in jdata and me.id in [user.get("id") for user in jdata["entities"]["user_mentions"]]:
                title = "@{screen_name}からリプライされました".format(**jdata["user"])
                body  = jdata["text"]
                pusher.push_note(title, body)
            elif "direct_message" in jdata:
                title = "@{screen_name}からDMが来ました".format(**jdata["direct_message"]["sender"])
                body  = jdata["text"]
                pusher.push_note(title, body)
        except KeyError:
            pass

    def on_error(self, status):
        print(status)

if __name__ == "__main__":
    stream = Stream(auth, TwitterEventListener())
    stream.userstream()
