from requests import get as _get
import datetime as dt
from json import dumps, load, loads, dump
from calendar import timegm
from time import sleep
from ago import human
from sys import exit

import praw
r = praw.Reddit('VOD loader by /u/suudo')
with open("/home/steven/gdqauth.json") as f:
    auth = load(f)

r.set_oauth_app_info(**auth["login"])
r.set_access_credentials(**r.refresh_access_information(auth["token"]))

def get(*args, **kwargs):
    print(">> get({}, {})".format(repr(args), repr(kwargs)))
    return _get(*args, **kwargs)

def load_json_from_reddit(subreddit, wikipage, orempty=False):
    """Reads json from a reddit wiki page. Allows the use of # as a comment character"""
    try:
        page = r.get_wiki_page(subreddit, wikipage).content_md
    except praw.errors.NotFound:
        if orempty:
            return {}
        raise
    return loads("\r\n".join([line.partition("#")[0].rstrip() for line in page.split("\r\n")]))

def dump_json_to_reddit(data, subreddit, wikipage):
    """Dumps json to a reddit wiki page.
    :param data: Arbitrary data that json.dumps can interpret
    :param subreddit: Destination subreddit
    :param wikipage: Destination wikipage"""
    return r.get_wiki_page(subreddit, wikipage).edit("\r\n".join("    "+l for l in json.dumps(data, indent=4).split("\n")))

out = {"info": {"site": "http://gamesdonequick.com/schedule",
                "author": "blha303",
                "email": "stevensmith.ome+gdq@gmail.com",
                "timezone": "UTC/GMT",
                "generated": [dt.datetime.utcnow().ctime(), timegm(dt.datetime.utcnow().utctimetuple())],
                "script": "https://b303.me/gdq/schedule.py",
                "raw": "https://b303.me/gdq/schedule.json",
                "vods": "https://b303.me/gdq/vods.md",
                "slug": "sgdq2017",
                "header": "https://www.reddit.com/r/suudo/wiki/gdqheader",
                "twitch": "http://twitch.tv/gamesdonequick"},
       "current": {},
       "schedule": []
      }

vods = load_json_from_reddit("suudo", out["info"]["slug"] + "vods")
urls = load_json_from_reddit("suudo", "gdqrunners")
runners = {r["pk"]:r["fields"] for r in get("https://gamesdonequick.com/tracker/search/?type=runner").json()}
event = [e for e in get("https://gamesdonequick.com/tracker/search/?type=event").json() if e["fields"]["short"] == out["info"]["slug"]][0]
with open("srcomgames.json") as f:
    games = load(f)

def splitnames(strlist):
    tmp = strlist.replace(", ", ";").replace(" and ", ";").replace(" vs ", ";").replace(" vs. ", ";").replace(";and ", ";").replace(" or maybe ", ";").replace("/", ";").replace(" ", "_").strip().split(";")
    return [] if not tmp[0] else tmp

def get_runners(id_list):
    out = {}
    for id in id_list:
        if id in runners:
            out[runners[id]["name"]] = runners[id]["stream"] or \
                ("https://www.youtube.com/user/{}".format(runners[id]["youtube"]) if runners[id]["youtube"] else "") or \
                ("https://twitter.com/{}".format(runners[id]["twitter"]) if runners[id]["twitter"] else "")
    return out

def get_srcom_info(data):
    out = {}
    api_url = "http://www.speedrun.com/api/v1"
    if data["game"] in games:
        out["srcom"] = games[data["game"]]
    elif "SETUP BLOCK" in data["game"]:
        out["srcom"] = {}
        out["wr"] = []
    else:
        resp = get(api_url + "/games", params={"name": data["game"], "embed": "categories"}).json().get("data")
        if resp:
            resp = {"id": resp[0]["id"], "categories": {i["name"]:i["id"] for i in resp[0]["categories"]["data"]}}
        else:
            out["srcom"] = {}
            out["wr"] = []
        games[data["game"]] = out["srcom"] = resp
    if out["srcom"]:
        if "records" in out["srcom"]:
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
        data["until"] = human(dt.datetime.now() - ts)
        data["game"] = data["tracker"]["name"]
        data["runners"] = get_runners(data["tracker"]["runners"])
        template_extra = ") [\\[{}\\]](http://twitch.tv/videos/{}?t={}"
        data["vod"] = ("http://twitch.tv/videos/{}?t={}".format(*vods[n][:2]) +
                       (template_extra.format(2, *vods[n][2:4])
                         if len(vods[n]) > 2 else "") +
                       (template_extra.format(3, *vods[n][4:6])
                         if len(vods[n]) > 4 else "")
                    if len(vods) > n else "http://twitch.tv/gamesdonequick")
#        data.update(get_srcom_info(data))
        if not out["current"] and "in " in data["until"]:
            out["current"].update(data)
        out["schedule"].append(data)
    out["schedule"].append({
        "game": "Finale!",
        "vod": "http://twitch.tv/videos/{}?t={}".format(*vods[-1][:2]) if len(vods) > len(gdq_data) else out["info"]["twitch"],
        "runTime": "forever",
        "runners": {"everyone": out["info"]["twitch"]}
    })
    out["current"]["donation"] = {"total": event["fields"]["amount"], "max": event["fields"]["max"], "avg": event["fields"]["avg"]}
    try:
        twitchd = get("https://api.twitch.tv/kraken/streams/gamesdonequick").json()["stream"]
        if twitchd:
            out["current"]["viewers"] = twitchd["viewers"]
        else:
            out["current"]["viewers"] = 0
    except:
        out["current"]["viewers"] = 0
    with open('schedule.json', 'w') as f:
        dump(out, f, indent=4)
    with open("srcomgames.json", "w") as f:
        dump(games, f)


if __name__ == "__main__":
    main()
