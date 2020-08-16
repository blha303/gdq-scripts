#/var/www/html/gdq/newpraw/bin/python
import praw, json
with open("/home/steven/gdqauth.json") as f:
    auth = json.load(f)
r = praw.Reddit(user_agent='GDQ thread autoupdater by /u/suudo', refresh_token=auth["token"], **auth["login"])

def load_json_from_reddit(subreddit, wikipage, orempty=False):
    """Reads json from a reddit wiki page. Allows the use of # as a comment character"""
    try:
        page = r.subreddit(subreddit).wiki[wikipage].content_md.replace("\r\n", "\n")
    except praw.errors.NotFound:
        if orempty:
            return {}
        raise
    wiki_data = "\n".join([line.partition("#")[0].rstrip() for line in page.split("\n")])
    return json.loads(wiki_data)

def dump_json_to_reddit(data, subreddit, wikipage):
    """Dumps json to a reddit wiki page.
    :param data: Arbitrary data that json.dumps can interpret
    :param subreddit: Destination subreddit
    :param wikipage: Destination wikipage"""
    return r.get_wiki_page(subreddit, wikipage).edit("\r\n".join("    "+l for l in json.dumps(data, indent=4).split("\n")))

variables = load_json_from_reddit("VODThread", "gdqvariables")

with open("vods.md") as f:
    d = f.read()
    thread = r.submission(variables["thread"]).selftext
    if thread != d:
        r.submission(variables["thread"]).edit(d)
        r.subreddit("VODThread").wiki["{}vodbak".format(variables["slug"])].edit(d)
