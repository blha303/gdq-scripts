all: schedule_json vod_thread updatethread

schedule_json:
	python3 schedule.py

vod_thread:
	python3 genvods.py

updatethread:
	python3 updatethread.py
