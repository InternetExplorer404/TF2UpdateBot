import feedparser
import time
import requests
import json
import tweepy

# Twitter credentials
twitter_enabled = False
consumer_key = None
consumer_secret = None
key = None
secret = None

if twitter_enabled is True:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)
    api = tweepy.API(auth)

url = "DISCORD'S WEBHOOK HERE"
last_update = None
update_loop = 60

def send_request(url, dict_embed):
    res = requests.post(url, data=json.dumps(dict_embed), headers={"Content-Type": "application/json"})
    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    return res.status_code


if __name__ == "__main__":
    while True:
        feed_entries = feedparser.parse("https://www.teamfortress.com/rss.xml")["entries"]
        if feed_entries[0]["title"] == "Team Fortress 2 Update Released" and feed_entries[0]["link"] != last_update:
            data = {}
            data["embeds"] = [{"title":feed_entries[0]["title"],
                               "description":"**" + feed_entries[0]["summary"].replace("<ul>", "").replace("</ul>", "").replace("<li>", "").replace("</li>", "").replace("<br />", "") + "**",
                               # THIS TERRIFIES ME. Someday I'll make a regex for this shit or something.
                               "color": 11751965,
                               "footer": {
                                   "text":feed_entries[0]["published"]
                               }
                               }]
            if twitter_enabled is True:
                api.update_status(f"SÍ\n{feed_entries[0]['link']}")

            status = send_request(url, data)
            last_update = feed_entries[0]["link"]
        time.sleep(update_loop)

