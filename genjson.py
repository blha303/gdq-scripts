#!/usr/bin/env python3
from json import load
with open("schedule.json") as f:
    schedule = load(f)

import praw
import prawcore
with open("/home/steven/gdqauth.json") as f:
    auth = load(f)
r = praw.Reddit(user_agent='VOD loader by /u/suudo', refresh_token=auth["token"], **auth["login"])

page = r.subreddit("VODThread").wiki[schedule["info"]["slug"] + "vods"]
try:
    _ = page.content_md
    if not _:
        raise prawcore.exceptions.NotFound(None)
except prawcore.exceptions.NotFound:
    page.edit("    [\n" + "\n".join("        [], # {}".format(x["game"]) for x in schedule["schedule"]) + "\n    ]")
    print("https://reddit.com/r/VODThread/wiki/{}vods".format(schedule["info"]["slug"]))

