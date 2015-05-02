#!/bin/bash
python ~/src/bar/server.py > logs/server.log &
echo "$!" > /tmp/bar_pidfile
sleep .1
python ~/src/bar/modules/timeblock.py > logs/timeblock.log &
python ~/src/bar/modules/ping.py > logs/ping.log &
python ~/src/bar/modules/df.py > logs/df.log &
python ~/src/bar/modules/mpd.py > logs/mpd.log &
python ~/src/bar/modules/load.py > logs/load.log &
wait
