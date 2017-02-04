from requests import get
from bs4 import BeautifulSoup as Soup
import datetime as dt
from json import dumps, load, loads, dump
from calendar import timegm
from time import sleep
from ago import human
from sys import exit

import praw
r = praw.Reddit('VOD loader by /u/suudo')
with open("/home/sites/gdqauth.json") as f:
    auth = load(f)

r.set_oauth_app_info(**auth["login"])
r.set_access_credentials(**r.refresh_access_information(auth["token"]))

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

vods = load_json_from_reddit("suudo", "agdq2017vods")
urls = load_json_from_reddit("suudo", "gdqrunners")
with open("srcomgames.json") as f:
    games = load(f)

out = {"info": {"site": "http://gamesdonequick.com/schedule",
                "author": "blha303",
                "email": "stevensmith.ome+gdq@gmail.com",
                "timezone": "UTC/GMT",
                "generated": [dt.datetime.utcnow().ctime(), timegm(dt.datetime.utcnow().utctimetuple())],
                "pretty": "https://b303.me/gdq/",
                "script": "https://b303.me/gdq/schedule.py",
                "raw": "https://b303.me/gdq/schedule.json",
                "vods": "https://b303.me/gdq/vods.md",
                "slug": "agdq2017",
                "header": "https://www.reddit.com/r/suudo/wiki/gdqheader"},
       "current": {},
       "schedule": []
      }

def splitnames(strlist):
    tmp = strlist.replace(", ", ";").replace(" and ", ";").replace(" vs ", ";").replace(" vs. ", ";").replace(";and ", ";").replace(" or maybe ", ";").replace("/", ";").replace(" ", "_").strip().split(";")
    return [] if not tmp[0] else tmp

def main():
    soup = Soup(get("http://www.gamesdonequick.com/schedule").text.replace("&#039;", "'").replace("&amp;", "&"), "html.parser")
    currentSet = False
    n = 0
    for row in soup.find('table', {'id': 'runTable'}).find('tbody').findAll('tr'):
        data = {}
        cols = row.findAll('td')
        if "class" in row.attrs:
            if "second-row" in row.attrs["class"]:
                data = out["schedule"][-1]
                data["runTime"] = cols[0].text.strip()
                data["category"] = cols[1].text.strip()
                api_url = "http://www.speedrun.com/api/v1"
                if data["game"] in games:
                    data["srcom"] = games[data["game"]]
                else:
                    resp = get(api_url + "/games", params={"name": data["game"], "embed": "categories"}).json()["data"]
                    if resp:
                        resp = {"id": resp[0]["id"], "categories": {i["name"]:i["id"] for i in resp[0]["categories"]["data"]}}
                        games[data["game"]] = data["srcom"] = resp
                    else:
                        data["srcom"] = {}
                        data["wr"] = []
                if data["srcom"]:
                    data["srcom_category"] = data["srcom"]["categories"].get(data["category"])
                    if data["srcom_category"]:
                        records = get(api_url + "/categories/{}/records".format(data["srcom_category"])).json()["data"]
                        if records and records[0]["runs"]:
                            wr = records[0]["runs"][0]["run"]
                            data["wr"] = [wr["weblink"] if "weblink" in wr else None, wr["times"]["primary_t"]]
                continue
            if "day-split" in row.attrs["class"]:
                continue
        try:
            ts = dt.datetime.strptime(cols[0].text, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            print(row)
            raise
        data["ts"] = timegm(ts.utctimetuple())
        data["time"] = cols[0].text
        data["until"] = human(dt.datetime.now() - ts)
        data["game"] = cols[1].text.strip()
        if data["game"] == "Finale!":
            data["runTime"] = "forever"
            data["category"] = "Any%"
        runners = {}
        for runner in splitnames(cols[2].text):
            runners[runner.replace("_", " ")] = urls[runner.replace("_", " ")] if runner.replace("_", " ") in urls else ("http://twitch.tv/" + runner) if runner not in ["None", "Everyone_still_awake"] else "http://twitch.tv/gamesdonequick"
        data["runners"] = runners
        data["setupTime"] = cols[3].text.strip() if len(cols) > 3 else ""
        template_extra = ") [\\[{}\\]](http://twitch.tv/gamesdonequick/v/{}?t={}"
        data["vod"] = ("http://twitch.tv/gamesdonequick/v/{}?t={}".format(*vods[n][:2]) +
                       (template_extra.format(2, *vods[n][2:4])
                         if len(vods[n]) > 2 else "") +
                       (template_extra.format(3, *vods[n][4:6])
                         if len(vods[n]) > 4 else "")
                    if len(vods) > n else "http://twitch.tv/gamesdonequick")
        if data["until"][:3] == "in " and not currentSet and len(out["schedule"]) > 0:
            out["current"] = dict()
            out["current"]["game"] = out["schedule"][-1]
            out["current"]["since"] = human(dt.datetime.now() - dt.datetime.strptime(out["schedule"][0]["time"], "%Y-%m-%dT%H:%M:%SZ"))
            out["current"]["donation"] = {}
            soup = Soup(get("https://gamesdonequick.com/tracker/index/{}".format(out["info"]["slug"])).text, "html.parser")
            out["current"]["donation"]["total"] = soup.find("small").text.strip().split("\n")[1].split(" ")[0]
            out["current"]["donation"]["maxavg"] = soup.find("small").text.strip().split("\n")[3]
            try:
                twitchd = get("https://api.twitch.tv/kraken/streams/gamesdonequick").json()["stream"]
                if twitchd:
                    out["current"]["viewers"] = twitchd["viewers"]
                else:
                    out["current"]["viewers"] = 0
            except:
                out["current"]["viewers"] = 0
            currentSet = True
        out["schedule"].append(data)
        n += 1
    with open('schedule.json', 'w') as f:
        dump(out, f, indent=4)
    with open("srcomgames.json", "w") as f:
        dump(games, f)


if __name__ == "__main__":
    main()
