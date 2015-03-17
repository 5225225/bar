import sys
import praw
import signal
import linelib


def handler(x, y):
    pass

signal.signal(signal.SIGUSR1, handler)
signal.signal(signal.SIGALRM, handler)

ID = "reddit"

r = praw.Reddit(user_agent="unread message checker by /u/5225225")
auth = open(sys.argv[1])
username, password = auth.read().split(":")
auth.close()
r.login(username, password.strip())

def sendline():
    try:
        x = r.get_unread(fetch=True)
    except requests.exceptions.HTTPError:
        #happens when reddit returns a 503. It should come back up soon.
        return
    x = list(x)
    if len(x) > 0:
        linelib.sendblock(ID, {"full_text": "[{}]".format(str(len(x))),
                               "color": "#ff4500"})
    linelib.sendPID(ID)
    linelib.waitsig(5)

while True:
    sendline()
