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
URL_PATTERN = re.compile("https://i.redd.it/.{13}.jpg")

for entry in parsed_feed.entries:
    content_value = entry.content[0].value
    try:
        image_url = URL_PATTERN.findall(content_value)[0]
        break
    except:
        continue

date = strftime("%Y-%m-%d", entry.updated_parsed)
title = entry.title
filename = f"{output}\\{date}_{title}.jpg"

print(f"{filename} | {image_url}")

with open(filename, 'wb') as handle:
    response = requests.get(image_url, stream=True)

    if not response.ok:
        print
        response

    for block in response.iter_content(1024):
        if not block:
            break

        handle.write(block)
