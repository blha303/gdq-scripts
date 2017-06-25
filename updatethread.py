import praw, sys, json
r = praw.Reddit('GDQ thread autoupdater by /u/suudo')
with open("/home/steven/gdqauth.json") as f:
    auth = json.load(f)

r.set_oauth_app_info(**auth["login"])
r.set_access_credentials(**r.refresh_access_information(auth["token"]))

post = r.get_submission("https://www.reddit.com/comments/6jd9qu")
with open("vods.md") as f:
    post.edit(f.read())
