from requests import get
from BeautifulSoup import BeautifulSoup as Soup
import datetime as dt
from json import dumps
from calendar import timegm
out = {"info": {"site": "http://gamesdonequick.com",
                "author": "blha303",
                "email": "b3@blha303.com.au",
                "pretty": "http://blha303.com.au/agdq/donations.html",
                "script": "http://blha303.com.au/agdq/donations.py",
                "json": "http://blha303.com.au/agdq/donations.json"},
       "donations": []}


def main():
    soup = Soup(get("http://www.gamesdonequick.com/tracker/donations/").text)
    arr = soup.find('table').findAll('tr')[1:]
    arr.reverse()
    for row in arr:
        cols = row.findAll('td')
        data = {}
        data["donor"] = {"url": out["info"]["site"] + cols[0].find('a')["href"], "name": cols[0].text.strip()}
        data["ts"] = timegm(dt.datetime.strptime(cols[1].text.strip(), "%m/%d/%Y %H:%M:%S +0000").utctimetuple())
        data["time"] = cols[1].text.strip()
        data["donation"] = {"url": out["info"]["site"] + cols[2].find('a')["href"], "name": cols[2].text.strip()}
        data["comment"] = True if cols[3].text.strip() == "Yes" else False
        out["donations"].append(data)
#        print "Done " + data["game"]
    with open('donations.json', 'w') as f:
        f.write(dumps(out))
#    print "Done."


if __name__ == "__main__":
    main()
