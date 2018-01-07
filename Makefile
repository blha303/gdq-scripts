thread: schedulejson vodthread updatethread

clean:
	rm runners.json events.json

runners.json:
	curl https://gamesdonequick.com/tracker/search/?type=runner -o runners.json

events.json:
	curl https://gamesdonequick.com/tracker/search/?type=event -o events.json

getdata: runners.json events.json

schedulejson: getdata
	python3 schedule.py

vodthread:
	python3 genvods.py

updatethread: newpraw
	newpraw/bin/python updatethread.py

requirements:
	pip3 install -r requirements.txt

newpraw:
	virtualenv newpraw
	newpraw/bin/pip install praw
