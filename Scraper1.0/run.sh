#!/bin/sh
pwd
ls
sleep 60
cd Documents/NHL-Score-Scraper/Scraper1.0
amixer -D pulse sset Master 100%
/usr/bin/python /home/nhl/Documents/NHL-Score-Scraper/Scraper1.0/scraper.py &
