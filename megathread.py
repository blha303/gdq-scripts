#!/var/www/html/gdq/newpraw/bin/python
import praw, json, time, traceback
with open("/home/steven/gdqauth.json") as f:
    auth = json.load(f)

r = praw.Reddit(user_agent='GDQ thread autoupdater by /u/suudo', refresh_token=auth["token"], **auth["login"])
with open("/var/www/html/gdq/schedule.json") as f:
  data = json.load(f)
  
if not hasattr(__builtins__, "raw_input"):
  raw_input = input

s = r.submission(raw_input("Enter submission ID: "))
comments = []

for d in data["schedule"]:
  while True:
    try:
      _ = s.reply("""**[{}]({})** run by {}{}""".format(d["game"], d["vod"], ", ".join("[{}]({})".format(k,v) for k,v in d["runners"].items()), " [YT]({})".format(d["yt"]) if d["yt"] and type(d["yt"]) is str else "" ))
    except:
      traceback.print_exc()
      continue
    break
  print("Posted {} {}".format(d["game"], _.id))
  comments.append(("**{}** run by {}".format(d["game"], ", ".join("[{}]({})".format(k,v) for k,v in d["runners"].items())), _))
  time.sleep(10)

s.edit("Find your favorite run below and upvote it!\r\n\r\n" + "\n".join("* {} [-->](https://reddit.com/r/{}/comments/{}/_/{})".format(d, s.subreddit.display_name, s.id, c.id) for d,c in comments ))
