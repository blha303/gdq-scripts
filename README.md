gdq-scripts
===========

A collection of scripts that make the [GDQ VOD threads](https://www.reddit.com/r/VODThread) easier.

Setup
-----

Currently setting up automatic VOD thread updating is somewhat difficult, at least I'm assuming it is because I haven't had to do it from scratch before. The scripts use several reddit wiki pages as configuration and data input, this was so it could be easily crowd-sourced as I was losing interest in watching hours of video to update the thread myself. The wiki pages being accessed are:

* [XgdqYYYYvods](https://reddit.com/r/VODThread/wiki/agdq2017vods), a JSON list of value pairs representing a Twitch VOD url for each of the runs in the [schedule](https://gamesdonequick.com/schedule). This needs to be manually updated for each new year
* ~~[gdqrunners](https://reddit.com/r/VODThread/wiki/gdqrunners), a mapping of usernames to their video URLs. needed because most runners use a slightly different username on the schedule to what they use on twitch~~
  * No longer needed, https://gamesdonequick.com/tracker/search/?type=runner
* [gdqvariables](https://www.reddit.com/r/VODThread/wiki/gdqvariables), containing previously hard-coded values that are used in the creation of the vod thread. An initial effort at making the entire script configurable from reddit wiki pages
* [gdqheader](https://www.reddit.com/r/VODThread/wiki/gdqheader), text inserted at the top of the vod thread containing a brief statement from the author and relevant links

In addition, `schedule.py` needs a file named `srcomgames.json` containing, initialy, an empty list (`[]`); this then gets populated with cache data for the world record column in the vod thread. Also, `updatethread.py` needs to be updated with the URL to the thread to be updated. These functions are separated so any one of them can be skipped and old data used to save time in development. There is a Makefile included that can simplify file generation.

Usage
-----

* `git clone https://github.com/blha303/gdq-scripts && cd gdq-scripts`
* (optional but recommended) `sudo pip3 install virtualenv && virtualenv ~/.gdqenv -p python3 && source ~/.gdqenv/bin/activate`
* `make requirements`
* Create an [personal use script application on reddit](https://www.reddit.com/prefs/apps/). The only required fields are name and redirect uri, set the latter to http://localhost
* Run the below code in your python interpreter to generate the authorization token for future use, swapping in your own `client_id`, `client_secret` and `redirect_uri` on line 4:

```python
import praw
import json
r = praw.Reddit("oauth token generator by /u/suudo")
auth = {"login": {"client_id": "kaODTxUZk3hcBQ", "client_secret": "PRIVATE", "redirect_uri": "http://localhost"}}
r.set_oauth_app_info(**auth["login"])
print(r.get_authorize_url("oauth", "edit read save wikiread", True))
# visit the above url, authorize it for your account, then copy the code from the url (e.g http://localhost/?state=oauth&code=<code>)
auth["token"] = r.get_access_information("<code>")["refresh_token"]
with open("gdqauth.json", "w") as f:
    json.dump(auth, f)
```

* `echo '[]' > srcomgames.json`
* Edit `schedule.py`:

  * On line 12, change the path to gdqauth.json. Make sure it's not web accessible!
  * On line 35, update the name of the event and create the relevant wiki page
  * On line 40, edit the links if you like, make sure to change the event slug
  * ~~If the loop from line 63 down fails, GDQ has probably changed the schedule page again. You'll have to figure out how to work around their alterations.~~
    * No longer needed, https://gamesdonequick.com/tracker/search/?type=run&event=20

* Edit `genvods.py`:

  * On line 3, change the path to gdqauth.json. Make sure it's not web accessible!

* Edit `updatethread.py`:

  * On line 3, change the path to gdqauth.json. Make sure it's not web accessible!
  * On line 9, change the URL to the active vod thread

* Update r/vodthread wiki pages gdqheader and gdqvariables to contain the correct links, thread ID and slug. I'd suggest using a test thread on r/vodthread for the first run.

* Run `make`. It should create `schedule.json` containing all data for creation of the vod thread, `vods.md` containing the actual text of the vod thread, and then push `vods.md` to the given reddit post.
* Run `make genjson` to create XgdqYYYYvods, then edit the second to last line to remove the comma (TODO: fix that lol)

Thanks
------

To StackOverflow contributors, my personal heroes.
