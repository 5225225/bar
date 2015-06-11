#!/bin/sh

cd ~/src/bar

./stop.sh
nohup ./start.sh 2>/dev/null &

python -u client.py

./stop.sh
