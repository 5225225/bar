import signal
import linelib
import subprocess


class filesystem:
    def __init__(self, device, total, used, free, mount):
        self.device = device
        self.total = total
        self.used = used
        self.free = free
        self.mount = mount


def fsfromline(line):
    x = line.split()
    print(x)
    return filesystem(x[0], x[1], x[2], x[3], x[5])


def handler(x, y):
    pass

signal.signal(signal.SIGUSR1, handler)
signal.signal(signal.SIGALRM, handler)

ID = "df"

wanted = ["/", "/home/jack/mount/NAS/downloads"]

names = {"/": "/", "/home/jack/mount/NAS/downloads": "NAS"}


while True:
    fslines = subprocess.check_output(["df", "-h"]).decode("utf-8").split("\n")
    fslines = fslines[1:-1]
    filesystems = []
    for line in fslines:
        fs = fsfromline(line)
        if fs.mount in wanted:
            filesystems.append(fs)

    blocks = []
    formatstr = "{}: {}/{}"
    for item in filesystems:
        blocks.append(formatstr.format(names[item.mount], item.used,
                                       item.total))

    linelib.sendblock(ID, {"full_text": " || ".join(blocks)})
    linelib.sendPID(ID)
    linelib.waitsig(1)
