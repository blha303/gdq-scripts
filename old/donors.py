from requests import get
from BeautifulSoup import BeautifulSoup as Soup
import datetime as dt
from json import dumps
from calendar import timegm
out = {"info": {"site": "http://gamesdonequick.com/tracker/donors/9?sort=total&order=-1&page=1",
                "author": "blha303",
                "baseurl": "http://gamesdonequick.com",
                "email": "b3@blha303.com.au",
                "pretty": "http://blha303.com.au/agdq/donors.html",
                "script": "http://blha303.com.au/agdq/donors.py",
                "json": "http://blha303.com.au/agdq/donors.json"},
       "donors": []}


def main():
    soup = Soup(get("http://www.gamesdonequick.com/tracker/donors/9?sort=total&order=-1&page=1").text)
    arr = soup.find('table').findAll('tr')[1:]
    for row in arr:
        cols = row.findAll('td')
        data = {}
        data["donor"] = {"url": out["info"]["baseurl"] + cols[0].find('a')["href"], "name": cols[0].text.strip(), "alias": cols[1].text.strip()}
        def clean(inp):
            return inp.strip().replace(",", "").replace("$", "")
        col2 = clean(cols[2].text).split(" (")
        col3 = clean(cols[3].text).split("/")
        data["donations"] = {"total": col2[0], "num": col2[1][:-1], "max": col3[0], "avg": col3[1]}
        out["donors"].append(data)
#        print "Done " + data["game"]
    with open('donors.json', 'w') as f:
        f.write(dumps(out))
#    print "Done."


if __name__ == "__main__":
    main()
