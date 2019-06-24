#!/usr/bin/env python
import requests, json
with open("events.json") as f:
    events = json.load(f)

pk = events[-1]["pk"]
d = requests.get("https://gamesdonequick.com/tracker/search/?type=run&event={}".format(pk)).json()
for x in d:
    print('        [], # {}'.format(x["fields"]["display_name"]))

