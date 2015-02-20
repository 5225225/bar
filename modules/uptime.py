import time
from datetime import timedelta

import linelib

while True:
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        uptime_string = timedelta(seconds=uptime_seconds)
    time.sleep(.01)
    linelib.sendblock("uptime", {"full_text": str(uptime_string)})
