#!/bin/bash
cd ~/.config/dtach/bar
python ~/src/bar/server.py &
sleep 1
python ~/src/bar/modules/timeblock.py & 
python ~/src/bar/modules/mpd.py &
python ~/src/bar/modules/load.py &
wait
