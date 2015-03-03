import signal
import linelib
import subprocess


def handler(x, y):
    pass


signal.signal(signal.SIGUSR1, handler)
signal.signal(signal.SIGALRM, handler)

ID = "ping"

toping = "8.8.8.8"

while True:
    raw = subprocess.check_output(["ping", "-c1", toping])
    line = raw.decode("UTF8").split("\n")[1]
    time = line.split(" ")[6][5:]
    linelib.sendblock(ID, {"full_text": "{}ms".format(time)})
    linelib.sendPID(ID)
    linelib.waitsig(5)
