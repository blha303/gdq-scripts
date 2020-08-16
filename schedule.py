from requests import get as _get
import datetime as dt
from json import dumps, load, loads, dump
from calendar import timegm
from time import sleep
from ago import human
from sys import exit

import praw
from prawcore.exceptions import NotFound

with open("/home/steven/gdqauth.json") as f:
  d = load(f)
  r = praw.Reddit(user_agent="VOD loader by u/suudo", refresh_token=d["token"], **d["login"])

def get(*args, **kwargs):
    print(">> get({}, {})".format(repr(args), repr(kwargs)))
    return _get(*args, **kwargs)

def load_json_from_reddit(subreddit, wikipage, orempty=None):
    """Reads json from a reddit wiki page. Allows the use of # as a comment character"""
    try:
        page = r.subreddit(subreddit).wiki[wikipage].content_md.replace("\r\n", "\n")
    except NotFound:
        if orempty:
            return orempty()
        raise
    wiki_data = "\n".join([line.partition("#")[0].rstrip() for line in page.split("\n")])
    return loads(wiki_data)

def dump_json_to_reddit(data, subreddit, wikipage):
    """Dumps json to a reddit wiki page.
    :param data: Arbitrary data that json.dumps can interpret
    :param subreddit: Destination subreddit
    :param wikipage: Destination wikipage"""
    return r.subreddit(subreddit).wiki[wikipage].edit("\r\n".join("    "+l for l in dumps(data, indent=4).split("\n")))

variables = load_json_from_reddit("VODThread", "gdqvariables")

out = {"info": {"site": "http://gamesdonequick.com/schedule",
                "author": "alyssadev",
                "email": "alyssa.dev.smith+gdq@gmail.com",
                "timezone": "UTC/GMT",
                "generated": [dt.datetime.utcnow().ctime(), timegm(dt.datetime.utcnow().utctimetuple())],
                "script": "https://b.suv.id.au/gdq/schedule.py",
                "raw": "https://b.suv.id.au/gdq/schedule.json",
                "vods": "https://b.suv.id.au/gdq/vods.md",
                "vodthread": "https://redd.it/{}".format(variables["thread"]),
                "slug": variables["slug"],
                "header": "https://reddit.com/r/VODThread/wiki/gdqheader",
                "twitch": "http://twitch.tv/gamesdonequick"},
       "current": {},
       "schedule": []
      }

vods = load_json_from_reddit("VODThread", out["info"]["slug"] + "vods", orempty=list)
urls = load_json_from_reddit("VODThread", "gdqrunners")
yt = load_json_from_reddit("VODThread", out["info"]["slug"] + "yt", orempty=dict)
donation_totals = load_json_from_reddit("VODThread", out["info"]["slug"] + "donations", orempty=list)
try:
    with open("runnerscache.json") as f:
        runners = load(f)
except:
    with open("runners.json") as f:
        runners = {str(r["pk"]):r["fields"] for r in load(f)}
with open("events.json") as f:
    event = [e for e in load(f) if e["fields"]["short"] == out["info"]["slug"]][0]
with open("srcomgames.json") as f:
    games = load(f)

def splitnames(strlist):
    tmp = strlist.replace(", ", ";").replace(" and ", ";").replace(" vs ", ";").replace(" vs. ", ";").replace(";and ", ";").replace(" or maybe ", ";").replace("/", ";").replace(" ", "_").strip().split(";")
    return [] if not tmp[0] else tmp

def get_runner(id):
    global runners
    runner = get("https://gamesdonequick.com/tracker/search/?type=runner&id={}".format(id)).json()[0]
    runners[str(id)] = runner["fields"]
    with open("runnerscache.json", "w") as f:
        dump(runners,f)
    return runner["fields"]

def get_runners(id_list):
    out = {}
    for id in id_list:
        if str(id) in runners:
            data = runners[str(id)]
        else:
            data = get_runner(id)
        out[data["name"]] = data["stream"].replace("htttp", "http") or \
            ("https://youtube.com/user/{}".format(data["youtube"]) if data["youtube"] else "") or \
            ("https://twitter.com/{}".format(data["twitter"]) if data["twitter"] else "")
    return out

def get_srcom_info(data):
    out = {}
    api_url = "http://speedrun.com/api/v1"
    if data["game"] in games:
        out["srcom"] = games[data["game"]]
    elif "SETUP BLOCK" in data["game"]:
        out["srcom"] = {}
        out["wr"] = []
    else:
        resp = get(api_url + "/games", params={"name": data["game"], "embed": "categories"}).json().get("data")
        if resp:
            resp = {"id": resp[0]["id"], "weblink": resp[0]["weblink"], "categories": {i["name"]:i["id"] for i in resp[0]["categories"]["data"]}}
        else:
            out["srcom"] = {}
            out["wr"] = []
        if type(resp) is dict:
            out["srcom"] = resp
        games[data["game"]] = resp
    if out["srcom"]:
        if "records" in out["srcom"] or not "categories" in out["srcom"]:
            return out
        out["srcom_category"] = out["srcom"]["categories"].get(data["category"])
        if out["srcom_category"]:
            records = get(api_url + "/categories/{}/records".format(out["srcom_category"])).json()["data"]
            out["srcom"]["records"] = records
            if records and records[0]["runs"]:
                wr = records[0]["runs"][0]["run"]
                out["wr"] = [wr["weblink"] if "weblink" in wr else None, wr["times"]["primary_t"]]
    return out

def main():
    gdq_data = get("https://gamesdonequick.com/tracker/search/?type=run&event={}".format(event["pk"])).json()
    for n, run in enumerate(gdq_data):
        data = {}
        data["tracker"] = run["fields"]
        data["runTime"] = data["tracker"]["run_time"]
        data["category"] = data["tracker"]["category"]
        ts = dt.datetime.strptime(data["tracker"]["starttime"], "%Y-%m-%dT%H:%M:%SZ")
        data["ts"] = timegm(ts.utctimetuple())
        data["time"] = data["tracker"]["starttime"]
        data["until"] = human(dt.datetime.utcnow() - ts)
        data["game"] = data["tracker"]["name"]
        data["runners"] = get_runners(data["tracker"]["runners"])
        template_extra = ") [\\[{}\\]](http://twitch.tv/videos/{}?t={}"
        if len(vods) > n and len(vods[n]) > 0:
            data["vod"] = "http://twitch.tv/videos/{}?t={}".format(*vods[n][:2]) + \
                           (template_extra.format(2, *vods[n][2:4])
                             if len(vods[n]) > 2 else "") + \
                           (template_extra.format(3, *vods[n][4:6])
                             if len(vods[n]) > 4 else "")
        else:
            data["vod"] = "http://twitch.tv/gamesdonequick"
        if len(yt) > n and len(yt[n]) > 0:
            if type(yt[n]) is list:
                data["yt"] = "http://youtu.be/{}) [YT](http://youtu.be/".format(yt[n][0]) + ") [YT](http://youtu.be/".join(yt[n][1:])
            else:
                data["yt"] = "http://youtu.be/{}".format(yt[n])
#        if len(yt) > n and len(yt[n]) > 0:
#            data["yt"] = "http://youtu.be/" + yt[n]
        else:
            data["yt"] = None
        if len(donation_totals) > n and len(donation_totals[n]) > 0:
            data["donation_total"] = donation_totals[n]
        else:
            data["donation_total"] = None
        data.update(get_srcom_info(data))
        data["current"] = False
        if not out["current"] and "in " in data["until"] and out["schedule"]:
            out["schedule"][-1]["current"] = True
            out["current"].update(out["schedule"][-1])
        out["schedule"].append(data)
    with open("srcomgames.json", "w") as f:
        dump(games, f)
    out["current"]["donation"] = get("https://gamesdonequick.com/tracker/event/{}?json".format(variables["slug"])).json()
    with open('schedule.json', 'w') as f:
        dump(out, f, indent=4)


if __name__ == "__main__":
    main()
