#!/bin/bash
DATE=$(date +"%Y%m%d%-H%M")

sqlite3 -header -csv datalog.db "select * from temp;" > $DATE.csv

wput /home/pi/$DATE.csv ftp://USER:PASSWORD@voresserver.dk/sommerhus/
