import signal
import linelib


def handler(x, y):
    pass

signal.signal(signal.SIGUSR1, handler)
signal.signal(signal.SIGALRM, handler)

ID = "template"

while True:
    with open("/proc/loadavg") as f:
        (min1, min5, min15, tasks, maxpid) = f.read().split(" ")
    linelib.sendblock(ID, {"full_text": min1})
    linelib.sendPID(ID)
    linelib.waitsig(1)
