from json import load
with open("/home/sites/gdqauth.json") as fb:
    auth = load(fb)
import praw
r = praw.Reddit('GDQ VOD thread generator by /u/suudo')
r.set_oauth_app_info(**auth["login"])
r.set_access_credentials(**r.refresh_access_information(auth["token"]))
joiner = "Game | Runner / Channel | Time / Link\r\n--|--|--|"

temp = "%s | %s | [%s](%s)"
usertemp = "[{name}]({url})"

with open("schedule.json") as fb:
    a = load(fb)

output = [r.get_wiki_page("suudo", "gdqheader").content_md + "\r\n\r\n" + joiner]
for i,q in enumerate(a["schedule"]):
    if q["vod"] == "http://twitch.tv/gamesdonequick":
        output[-1] = output[-1].replace(a["schedule"][i-1]["runTime"], "*{}*".format(a["schedule"][i-1]["runTime"]))
    output.append(temp % (q["game"] + (" ({})".format(q["category"]) if "category" in q and q["category"] and q["category"] != "Any%" else ""),
                          ", ".join([usertemp.format(name=k, url=v) for k,v in q["runners"].items()]),
                          "~~{}~~".format(q["runTime"]) if q["vod"] == "http://twitch.tv/gamesdonequick" else q["runTime"],
                          q["vod"]) )

with open("vods.md", "w") as f:
    f.write("\r\n".join(output))
