#!/bin/bash
python ~/src/bar/server.py &
echo "$!" > pidfile
sleep .1
python ~/src/bar/modules/timeblock.py & 
python ~/src/bar/modules/mpd.py &
python ~/src/bar/modules/load.py &
python ~/src/bar/modules/reddit.py modules/reddit-auth &
wait
