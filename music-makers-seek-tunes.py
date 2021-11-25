# https://stackoverflow.com/a/55804977

import tweepy
import logging
import os

logger = logging.Logger("info")

user_name = "@ThatKevinSmith"
tweet_id = "1461361593564811278"

consumer_key = os.environ.get("TWITTER_API_KEY")
consumer_secret = os.environ.get("TWITTER_API_KEY_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

api = tweepy.API(auth)

replies = tweepy.Cursor(
    api.search_tweets,
    q="to:{}".format(user_name),
    since_id=tweet_id,
    tweet_mode="extended",
).items()

count = 0

music_makers_seek_tunes = open("music-makers-seek-tunes.html", "w")

while True:
    try:
        count += 1
        reply = replies.next()
        print(
            "%s. %s %s\n"
            % (
                count,
                reply._json["user"]["screen_name"],
                reply._json["full_text"],
            )
        )
        if not hasattr(reply, "in_reply_to_status_id_str"):
            continue
        if reply.in_reply_to_status_id == tweet_id:
            logging.info("reply of tweet:{}".format(reply.full_text))

    except StopIteration:
        break

    except Exception as e:
        logger.error("Failed while fetching replies {}".format(e))
        break
