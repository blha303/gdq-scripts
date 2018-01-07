#/var/www/html/gdq/newpraw/bin/python
import praw, json
with open("/home/steven/gdqauth.json") as f:
    auth = json.load(f)
r = praw.Reddit(user_agent='GDQ thread autoupdater by /u/suudo', refresh_token=auth["token"], **auth["login"])

with open("vods.md") as f:
    r.submission("7oljmp").edit(f.read())
