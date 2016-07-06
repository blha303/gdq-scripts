import praw, sys, json
r = praw.Reddit('GDQ thread autoupdater by /u/suudo')
with open("/home/sites/gdqauth.json") as f:
    auth = json.load(f)

r.set_oauth_app_info(**auth["login"])
r.set_access_credentials(**r.refresh_access_information(auth["token"]))

joiner = "Game | Runner / Channel | Time / Link\r\n--|--|--|--|"

post = r.get_submission("https://www.reddit.com/comments/4r4pyp")
comment1 = r.get_submission("https://www.reddit.com/comments/4r4pyp/_/d4y9soi").comments[0]
comment2 = r.get_submission("https://www.reddit.com/comments/4r4pyp/_/d4y9u4g").comments[0]
#comment3 = r.get_submission("https://www.reddit.com/comments/4r4pyp/_/cyk9qk7").comments[0]
with open("vods.md") as f:
    data = f.read()

def splitter(md):
    outp = ""
    postnum = 1
    for line in md.split("\r\n"):
        if len(outp) > 19500:
            if postnum is 1:
                outp += u"\r\n\r\nContinued in " + comment1.permalink
                if post.selftext != outp:
                    post.edit(outp)
                outp = joiner
                postnum = 2
            elif postnum is 2:
                outp += u"\r\n\r\nContinued in " + comment2.permalink
                if comment1.body != outp:
                    comment1.edit(outp)
                outp = joiner
                postnum = 3
            elif postnum is 3:
#                outp += u"\r\n\r\nContinued in " + comment3.permalink
                if comment2.body != outp:
                    comment2.edit(outp)
                outp = joiner
                postnum = 4
            elif postnum is 4:
                outp += u"\r\n\r\nContinued in " + comment4.permalink
                if comment3.body != outp:
                    comment3.edit(outp)
                outp = joiner
                postnum = 5
#            elif postnum is 5:
                from singlemessagebot import SingleMessageBot
                bot = SingleMessageBot("blha303: We got a problem. Add more comments.")
                bot.start()
                sys.exit(2)
        if not outp:
            outp = line
        else:
            outp += "\r\n" + line
#        print line
    if outp:
        if postnum is 1:
            if post.selftext != outp:
                post.edit(outp)
        elif postnum is 2:
            if comment1.body != outp:
                comment1.edit(outp)
        elif postnum is 3:
            if comment2.body != outp:
                comment2.edit(outp)
        elif postnum is 4:
            if comment3.body != outp:
                comment3.edit(outp)
        elif postnum is 5:
            from singlemessagebot import SingleMessageBot
            bot = SingleMessageBot("blha303: We got a problem. Add more comments.")
            bot.start()
            sys.exit(2)
#        elif postnum is 5:
#            comment4.edit(outp)

if __name__ == "__main__":
    splitter(data)
