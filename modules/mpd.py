import socket
import signal
import linelib
import time
import json
ID = "mpd"

def darken(hexcode, amount=.5):
    r = int(int(hexcode[1:3], 16) * amount)
    g = int(int(hexcode[3:5], 16) * amount)
    b = int(int(hexcode[5:7], 16) * amount)
    return "#{:x}{:x}{:x}".format(r, g, b)



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
        time.sleep(1)
        return
    except OSError:
        time.sleep(1)
        return
    try:
        version = sock.recv(2048)
    except InterruptedError:
        pass

    assert version == b"OK MPD 0.19.0\n"

    sock.send(b"currentsong\n")
    currsong = mpd2dict(sock.recv(2048).decode("UTF-8"))

    if currsong == {}:
        return

    sock.send(b"status\n")
    status = mpd2dict(sock.recv(2048).decode("UTF-8"))

    infodict = currsong.copy()
    infodict.update(status)
    
    artistcolour = "#a1b56c"
    titlecolour = "#ac4142"
    albumcolour = "#6a9fb5"
    

    if infodict["state"] == "pause":
        titlecolour = darken(titlecolour)
        albumcolour = darken(albumcolour)
        artistcolour = darken(artistcolour)

    block = "<span foreground='{}'>{}</span>"
    
    for item in ["Artist", "Title", "Album"]:
        if item not in infodict:
            infodict[item] = "Unknown {}".format(item)

    fmline = "{} - {} - {}".format(
        block.format(artistcolour,infodict["Artist"]),
        block.format(titlecolour,infodict["Title"]),
        block.format(albumcolour,infodict["Album"]),
    )
    
    formatcodes = fmline.replace("&", "&amp;")
    linelib.sendblock(ID, {"full_text": formatcodes, "markup": "pango"})
    linelib.sendPID(ID)
    linelib.waitsig(1)
    click = linelib.getclick(ID).decode("UTF-8")
    if click != "":
        x = json.loads(click)
        if x["button"] == 1:
            sock.send(b"pause\n")

while True:
    sendline()
