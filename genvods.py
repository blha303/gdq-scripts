from json import load, loads
from datetime import timedelta
from random import choice
import praw
from prawcore.exceptions import NotFound

with open("/home/steven/gdqauth.json") as fb:
    d = load(fb)
    r = praw.Reddit(user_agent="VOD loader by u/suudo", refresh_token=d["token"], **d["login"])

def load_json_from_reddit(subreddit, wikipage, orempty=False):
    """Reads json from a reddit wiki page. Allows the use of # as a comment character"""
    try:
        page = r.subreddit(subreddit).wiki[wikipage].content_md.replace("\r\n", "\n")
    except NotFound:
        if orempty:
            return {}
        raise
    wiki_data = "\n".join([line.partition("#")[0].rstrip() for line in page.split("\n")])
    return loads(wiki_data)

def dump_json_to_reddit(data, subreddit, wikipage):
    """Dumps json to a reddit wiki page.
    :param data: Arbitrary data that json.dumps can interpret
    :param subreddit: Destination subreddit
    :param wikipage: Destination wikipage"""
    return r.subreddit(subreddit).wiki[wikipage].edit("\r\n".join("    "+l for l in dumps(data, indent=4).split("\n")))

vars = load_json_from_reddit("VODThread", "gdqvariables")

with open("schedule.json") as fb:
    a = load(fb)

quote = choice([x.strip() for x in r.subreddit("VODThread").wiki["gdqquotes"].content_md.split("\n")])
output = [r.subreddit("VODThread").wiki["gdqheader"].content_md + "\r\n\r\n" + vars["joiner"]]
for i,q in enumerate(a["schedule"]):
    if q["vod"] == "http://twitch.tv/gamesdonequick":
        output[-1] = output[-1].replace(a["schedule"][i-1]["runTime"], "*{}*".format(a["schedule"][i-1]["runTime"]))
    game = q["game"] + (" ({})".format(q["category"]) if "category" in q and q["category"] and q["category"] != "Any%" else "")
    if "srcom" in q and q["srcom"] and q["srcom"].get("weblink"):
        game = game + "^[+]({})".format(q["srcom"]["weblink"])
    runners = ", ".join(vars["user"].format(name=k, url=q["runners"][k]) if q["runners"][k] else k for k in sorted(q["runners"]))
    time = "~~{}~~".format(q["runTime"]) if q["vod"] == "http://twitch.tv/gamesdonequick" else q["runTime"]
    output.append((vars["row"] % (game + ("**<**" if q["current"] else ""), runners, time, q["vod"])) + (" [YT]({})".format(q["yt"]) if "yt" in q and q["yt"] else ""))

with open("vods.md", "w") as f:
    f.write("\r\n".join(output))
