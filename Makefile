thread: schedulejson vodthread updatethread

getdata:
	curl https://gamesdonequick.com/tracker/search/?type=runner -o runners.json
	curl https://gamesdonequick.com/tracker/search/?type=event -o events.json

schedulejson:
	python3 schedule.py

vodthread:
	python3 genvods.py

updatethread:
	python3 updatethread.py

requirements:
	pip install -r requirements.txt

vodjson:
	python3 genjson.py
