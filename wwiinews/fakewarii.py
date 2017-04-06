
import csv  # noqa
import html
import re
from time import sleep

from lxml import etree

import requests


def get_tweets(account):
    xml = requests.get(
            'https://twitrss.me/twitter_user_to_rss/?user=' +
            account).content

    tree = etree.fromstring(xml)
    for item in tree.cssselect('item description'):
        text = re.search('>([^<]+)', item.text).group(1)
        # if '<img' in item.text:
        #     img = re.search('<img.*>', item.text).group(0)
        for b in bad_words:
            if re.search(b, text, re.IGNORECASE):
                break
        else:

            yield html.unescape(text)

        # tweet = etree.fromstring(item.text)
        # print(tweet.cssselect("p").text)


def substitute():
    subs = {}
    with open('Subs.csv') as f:
        for line in f:
            subs.__setitem__(*line.strip().split(","))

    for tweet in get_tweets('realtimewwii'):
        old_tweet = tweet
        for word, sub in subs.items():
            if word in tweet:
                tweet = re.sub(word, sub, tweet)

        if tweet == old_tweet:
            continue

        yield tweet, old_tweet


def main():
    for tweet, old_tweet in substitute():
        print('', tweet, '\n============\n', old_tweet, '\n\n')
        sleep(2)


bad_words = [
    'bod(y|ies)',
    'charred',
    'child(ren)?',
    'civilians?',
    'japs?',
    'jews?',
    'suicid(e|al)',
]


if __name__ == "__main__":
    main()
