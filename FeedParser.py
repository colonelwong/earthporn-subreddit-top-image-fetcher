#! /usr/bin/python
import sys
import feedparser
import socket
import re
from time import strftime
import requests

timeout = 120
socket.setdefaulttimeout(timeout)

feed_url = sys.argv[1]
output = sys.argv[2]

parsed_feed = feedparser.parse(feed_url)

image_url = ""
for entry in parsed_feed.entries:
    content_value = entry.content[0].value
    pattern = "https://i.redd.it/.{13}.jpg"
    regex = re.compile(pattern)
    try:
        image_url = regex.findall(content_value)[0]
        break
    except:
        continue

date = strftime("%Y-%m-%d", entry.updated_parsed)
title = entry.title
filename = output + "\\" + date + "_" + title + ".jpg"

print(filename + " | " + image_url)

with open(filename, 'wb') as handle:
    response = requests.get(image_url, stream=True)

    if not response.ok:
        print
        response

    for block in response.iter_content(1024):
        if not block:
            break

        handle.write(block)
