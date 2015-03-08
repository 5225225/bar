import socket
import signal
import linelib
import time
import json
ID = "mpd"


def handler(x, y):
    pass

signal.signal(signal.SIGUSR1, handler)
signal.signal(signal.SIGALRM, handler)


def mpd2dict(output):
    x = output.split("\n")
    d = dict()
    for item in x[:-2]:
        # MPD returns OK at the end, and there's a newline. This skips both of
        # them.
        key, val = item.split(":", maxsplit=1)
        val = val.lstrip()
        d[key] = val
    return d

def sendline():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 6600))
    except ConnectionRefusedError:
        return

    version = sock.recv(2048)

    assert version == b"OK MPD 0.19.0\n"

    sock.send(b"currentsong\n")
    currsong = mpd2dict(sock.recv(2048).decode("UTF-8"))

    if currsong == {}:
        return

    sock.send(b"status\n")
    status = mpd2dict(sock.recv(2048).decode("UTF-8"))

    infodict = currsong.copy()
    infodict.update(status)

    titlecolour = "#ac4142"
    albumcolour = "#6a9fb5"

    dark_titlecolour = "#542020"
    dark_albumcolour = "#3c5a66"

    TC = str()
    AC = str()
    BC = str()

    if infodict["state"] == "pause":
        TC = dark_titlecolour
        AC = dark_albumcolour
    else:
        TC = titlecolour
        AC = albumcolour

    # TODO make this code not ugly

    formatcodes = "<span foreground='{}'>{}</span> - <span "\
        "foreground='{}'>{}</span>".format(TC, infodict["Title"], AC,
                                           infodict["Album"])

    linelib.sendblock(ID, {"full_text": formatcodes})
    linelib.sendPID(ID)
    linelib.waitsig(1)
    click = linelib.getclick(ID).decode("UTF-8")
    if click != "":
        x = json.loads(click)
        if x["button"] == 1:
            sock.send(b"pause\n")

while True:
    sendline()
