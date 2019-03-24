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
first_entry = parsed_feed.entries[0]

content_value = first_entry.content[0].value
pattern = "https://i.redd.it/.{13}.jpg"
regex = re.compile(pattern)

image_url = regex.findall(content_value)[0]
filename = strftime("%Y-%m-%d", first_entry.updated_parsed) + ".jpg"
filename_path = output + "\\" + filename

print(filename_path + " | " + image_url)

with open(filename_path, 'wb') as handle:
    response = requests.get(image_url, stream=True)

    if not response.ok:
        print
        response

    for block in response.iter_content(1024):
        if not block:
            break

        handle.write(block)