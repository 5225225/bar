import signal
import linelib


def handler(x, y):
    pass

signal.signal(signal.SIGUSR1, handler)
signal.signal(signal.SIGALRM, handler)

ID = "template"

while True:
    linelib.sendblock(ID, {"full_text": ""})
    linelib.sendPID(ID)
    linelib.waitsig(1)
