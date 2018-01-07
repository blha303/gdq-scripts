#!/usr/bin/env python3
from json import load
with open("schedule.json") as f:
    schedule = load(f)

import praw
r = praw.Reddit('VOD loader by /u/suudo')
with open("/home/steven/gdqauth.json") as f:
    auth = load(f)
r.set_oauth_app_info(**auth["login"])
r.set_access_credentials(**r.refresh_access_information(auth["token"]))

page = r.get_wiki_page("suudo", schedule["info"]["slug"] + "vods")
try:
    _ = page.content_md
    if not _:
        raise praw.errors.NotFound(None)
except praw.errors.NotFound:
    page.edit("    [\n" + "\n".join("        [], # {}".format(x["game"]) for x in schedule["schedule"]) + "\n    ]")
    print("https://reddit.com/r/suudo/wiki/{}vods".format(schedule["info"]["slug"]))

