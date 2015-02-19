import socket
import signal
import linelib

ID = "mpd"

def handler(x,y):
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

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 6600))

    version = sock.recv(2048)

    assert version == b"OK MPD 0.19.0\n"

    sock.send(b"currentsong\n")
    currsong = mpd2dict(sock.recv(2048).decode("UTF-8"))

    sock.send(b"status\n")
    status = mpd2dict(sock.recv(2048).decode("UTF-8"))


    infodict = currsong.copy()
    infodict.update(status)

    print(infodict)
    
    out = "{Title} - {Album} [{bitrate}kbps]".format(**infodict)

    titlecolour = "#ac4142"
    albumcolour = "#6a9fb5"
    bitratecolour = "#a1b56c"
    noformatting = "#dddddd"

    dark_titlecolour = "#542020"
    dark_albumcolour = "#3c5a66"
    dark_bitratecolour = "#4f5935"
    dark_noformatting = "#6e6e6e"

    TC = str()
    AC = str()
    BC = str()
    NF = str()

    if infodict["state"] == "pause":
        TC = dark_titlecolour
        AC = dark_albumcolour
        BC = dark_bitratecolour
        NF = dark_noformatting
    else:
        TC = titlecolour
        AC = albumcolour
        BC = bitratecolour
        NF = noformatting

    #TODO make this code not ugly

    titleblock = {"full_text": infodict["Title"],
                  "color": TC
        }

    albumblock = {"full_text": infodict["Album"],
                  "color": AC
        }



    sep = {"full_text":" - ",
        "color": NF
        }

    ob = {"full_text":" [",
        "color": NF }
    bitrate = {"full_text": infodict["bitrate"],
                  "color": BC
        }

    cb = {"full_text":"]",
        "color": NF
    }

    kbps = {"full_text":" kbps",
        "color": NF
    } 
    blocklist = [titleblock, sep, albumblock, ob, bitrate, kbps, cb]
    linelib.sendmultiblock(ID, blocklist)

    linelib.sendPID(ID)
    linelib.waitsig(1)
