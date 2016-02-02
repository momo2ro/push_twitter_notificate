from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy.streaming import StreamListener
import json

consumer_key        = ""
consumer_secret     = ""
access_token        = ""
access_token_secret = ""

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)
me = api.me()


class StdOutListener(StreamListener):
    def on_data(self, data):
        jdata = json.loads(data)
        try:
            if jdata.get("event") == "favorite" and jdata["source"]["id"] != me.id:
                print("@{screen_name}からふぁぼられました".format(**jdata["source"]))
            if jdata.get("event") == "unfavorite" and jdata["source"]["id"] != me.id:
                print("@{screen_name}からあんふぁぼされました".format(**jdata["source"]))
            elif jdata.get("event") == "follow":
                print("@{screen_name}からフォローされました".format(**jdata["source"]))
            elif jdata.get("event") == "unfollow":
                print("@{screen_name}からアンフォローされました".format(**jdata["source"]))
            elif "retweeted_status" in jdata and jdata["retweeted_status"]["user"]["id"] == me.id:
                print("@{screen_name}からRTされました".format(**jdata["user"]))
            elif "in_reply_to_user_id" in jdata and me.id in [user.get("id") for user in jdata["entities"]["user_mentions"]]:
                print("@{screen_name}からリプライされました".format(**jdata["user"]))
            elif "direct_message" in jdata:
                print("@{screen_name}からDMが来ました".format(**jdata["direct_message"]["sender"]))
        except KeyError:
            print("error")

    def on_error(self, status):
        print(status)

if __name__ == "__main__":
    stream = Stream(auth, StdOutListener())
    stream.userstream(replies="all")
