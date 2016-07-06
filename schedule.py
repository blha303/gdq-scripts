from requests import get
from bs4 import BeautifulSoup as Soup
import datetime as dt
from json import dumps, load, loads
from calendar import timegm
from time import sleep
from ago import human
from sys import exit

#from vods_agdq2016 import vods

import praw
r = praw.Reddit('VOD loader by /u/suudo')
with open("/home/sites/gdqauth.json") as f:
    auth = load(f)

r.set_oauth_app_info(**auth["login"])
r.set_access_credentials(**r.refresh_access_information(auth["token"]))

def load_json_from_reddit(subreddit, wikipage):
    page = r.get_wiki_page(subreddit, wikipage).content_md
    return loads("\r\n".join([line.partition("#")[0].rstrip() for line in page.split("\r\n")]))

vods = load_json_from_reddit("suudo", "sgdq2016vods")
urls = load_json_from_reddit("suudo", "gdqrunners")

out = {"info": {"site": "http://gamesdonequick.com/schedule",
                "author": "blha303",
                "email": "steven@b303.me",
                "timezone": "UTC/GMT",
                "generated": [dt.datetime.utcnow().ctime(), timegm(dt.datetime.utcnow().utctimetuple())],
                "pretty": "https://b303.me/gdq/",
                "script": "https://b303.me/gdq/schedule.py",
                "raw": "https://b303.me/gdq/schedule.json",
                "vods": "https://b303.me/gdq/vods.md",
                "slug": "sgdq2016",
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
                out["schedule"][-1]["runTime"] = cols[0].text.strip()
                out["schedule"][-1]["category"] = cols[1].text.strip()
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
        if data["until"][:3] == "in " and not currentSet:
            out["current"] = dict()
            out["current"]["game"] = out["schedule"][-1]
            out["current"]["since"] = human(dt.datetime.now() - dt.datetime.strptime(out["schedule"][0]["time"], "%Y-%m-%dT%H:%M:%SZ"))
            out["current"]["donation"] = {}
            soup = Soup(get("https://gamesdonequick.com/tracker/index/{}".format(out["info"]["slug"])).text, "html.parser")
            out["current"]["donation"]["total"] = soup.find("small").text.strip().split("\n")[1].split(" ")[0]
            out["current"]["donation"]["maxavg"] = soup.find("small").text.strip().split("\n")[3]
            twitchd = get("https://api.twitch.tv/kraken/streams/gamesdonequick").json()["stream"]
            if twitchd:
                out["current"]["viewers"] = twitchd["viewers"]
            else:
                out["current"]["viewers"] = 0
            currentSet = True
        out["schedule"].append(data)
        n += 1
    with open('schedule.json', 'w') as f:
        f.write(dumps(out))
    with open('bak/schedule.json.' + dt.datetime.strftime(dt.datetime.now(), "%Y%m%d-%H%M"), 'w') as f:
        f.write(dumps({'current': out["current"]}))


if __name__ == "__main__":
    main()
