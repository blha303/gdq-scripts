#!/bin/bash
cd /home/sites/blha303.com.au/gdq
python3 schedule.py && python3 genvods.py && python3 updatethread.py
