thread: schedulejson vodthread updatethread

clean:
	rm runners.json events.json

runners.json:
	curl https://gamesdonequick.com/tracker/search/?type=runner -o runners.json
	sed -i 's/www\.//g' runners.json

events.json:
	curl https://gamesdonequick.com/tracker/search/?type=event -o events.json

getdata: runners.json events.json

vodjson: events.json
	python3 vodjson.py

schedulejson: getdata
	newpraw/bin/python schedule.py

vodthread:
	newpraw/bin/python genvods.py

updatethread:
	newpraw/bin/python updatethread.py

requirements:
	pip3 install -r requirements.txt

newpraw:
	virtualenv newpraw
	newpraw/bin/pip install praw
