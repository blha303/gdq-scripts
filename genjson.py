#!/usr/bin/env python3
import json
with open("schedule.json") as f:
    schedule = json.load(f)

import praw
r = praw.Reddit('VOD loader by /u/suudo')
with open("/home/steven/gdqauth.json") as f:
    auth = load(f)
r.set_oauth_app_info(**auth["login"])
r.set_access_credentials(**r.refresh_access_information(auth["token"]))

page = r.get_wiki_page("suudo", out["info"]["slug"] + "vods")
try:
    _ = page.content_md
except praw.errors.NotFound:
    page.edit("    [\n" + "\n".join("        [], # {}".format(x["game"]) for x in schedule["schedule"]) + "\n    ]")
    print("https://reddit.com/r/suudo/wiki/{}vods".format(out["info"]["slug"]))

