from json import load, loads
from datetime import timedelta
with open("/home/sites/gdqauth.json") as fb:
    auth = load(fb)
import praw
r = praw.Reddit('GDQ VOD thread generator by /u/suudo')
r.set_oauth_app_info(**auth["login"])
r.set_access_credentials(**r.refresh_access_information(auth["token"]))

vars = loads("\r\n".join([line.partition("#")[0].rstrip() for line in r.get_wiki_page("suudo", "gdqvariables").content_md.split("\r\n")]))

with open("schedule.json") as fb:
    a = load(fb)

output = [r.get_wiki_page("suudo", "gdqheader").content_md + "\r\n\r\n" + vars["joiner"]]
for i,q in enumerate(a["schedule"]):
    if q["vod"] == "http://twitch.tv/gamesdonequick":
        output[-1] = output[-1].replace(a["schedule"][i-1]["runTime"], "*{}*".format(a["schedule"][i-1]["runTime"]))
    game = q["game"] + (" ({})".format(q["category"]) if "category" in q and q["category"] and q["category"] != "Any%" else "")
    runners = ", ".join([vars["user"].format(name=k, url=v) for k,v in q["runners"].items()])
    wr = "[{}]({})".format(str(timedelta(seconds=q["wr"][1])).split(".")[0], q["wr"][0]) if "wr" in q else "-"
    time = "~~{}~~".format(q["runTime"]) if q["vod"] == "http://twitch.tv/gamesdonequick" else q["runTime"]
    output.append(vars["row"] % (game, runners, wr, time, q["vod"]))

with open("vods.md", "w") as f:
    f.write("\r\n".join(output))
