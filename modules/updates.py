import signal
import linelib
import subprocess


def handler(x,y):
    pass

signal.signal(signal.SIGUSR1, handler)
signal.signal(signal.SIGALRM, handler)

ID = "updates"

while True:
    updates = subprocess.check_output(["/usr/bin/pacaur", "-Qua"]).decode("ASCII").strip().split("\n")
    linelib.sendblock(ID, {"full_text":str(len(updates))})
    linelib.sendPID(ID)
    linelib.waitsig(1)
