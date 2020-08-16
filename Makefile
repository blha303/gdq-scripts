thread: schedulejson vodthread updatethread

clean:
	rm runners.json events.json runnerscache.json

runners.json:
	curl https://gamesdonequick.com/tracker/search/?type=runner -o runners.json
	sed -i 's/www\.//g' runners.json

events.json:
	curl https://gamesdonequick.com/tracker/search/?type=event -o events.json

getdata: runners.json events.json

genjson:
	newpraw/bin/python genjson.py

schedulejson: getdata
	newpraw/bin/python schedule.py

vodthread:
	newpraw/bin/python genvods.py

updatethread:
	newpraw/bin/python updatethread.py

requirements:
	pip3 install -r requirements.txt

newpraw:
	virtualenv -p python3 newpraw
	newpraw/bin/pip install praw
