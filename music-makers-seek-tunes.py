# https://stackoverflow.com/a/55804977

import tweepy
import logging
import os

logger = logging.Logger("info")

user_name = "@ThatKevinSmith"
tweet_id = "1461361593564811278"

consumer_key = os.environ.get("TWITTER_API_KEY")
consumer_secret = os.environ.get("TWITTER_API_KEY_SECRET")
# access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
# access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

api = tweepy.API(auth)

replies = tweepy.Cursor(
    api.search_tweets,
    q="to:{}".format(user_name),
    since_id=tweet_id,
    tweet_mode="extended",
).items()
while True:
    try:
        reply = replies.next()
        print(reply)
        if not hasattr(reply, "in_reply_to_status_id_str"):
            continue
        if reply.in_reply_to_status_id == tweet_id:
            logging.info("reply of tweet:{}".format(reply.full_text))

    # except tweepy.errors.RateLimitError as e:
    #     logging.error("Twitter api rate limit reached".format(e))
    #     time.sleep(60)
    #     continue

    # except tweepy.errors.TweepError as e:
    #     logging.error("Tweepy error occured:{}".format(e))
    #     break

    except StopIteration:
        break

    except Exception as e:
        logger.error("Failed while fetching replies {}".format(e))
        break
