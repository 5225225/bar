import json
import socket
import time
import os
import signal


class block:
    def __init__(self, blockdict):
        self.toprint = {}
        self.atime = time.time()
        self.toprint["_timeout"] = 15
        for item in blockdict:
            self.toprint[item] = blockdict[item]

blocks = {}


def tojsonstr():
    x = []
    torm = []

    for ID in blocks:
        blocks[ID].ID = ID
        blocks[ID].toprint["name"] = ID

    for ID in blocks:
        currblock = blocks[ID]
        if currblock.atime + currblock.toprint["_timeout"] < time.time():
            torm.append(ID)

    for item in torm:
        del blocks[item]

    for ID in blocks:
        x.append(blocks[ID].toprint)

    return json.dumps(sorted(x, key=lambda block: block["name"]))

pids = {}
clicks = {}

# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to a public host, and a well-known port
serversocket.bind(("localhost", 1337))
# become a server socket
serversocket.listen(1)

while True:
    (cs, addr) = serversocket.accept()
    data = cs.recv(2048).decode("UTF-8")
    if data != "LINE":
        print(data)
    if data.startswith("LINE"):
        cs.send(tojsonstr().encode("UTF-8"))
        cs.close()
    elif data.startswith("BLOCK"):
        blockdata = data[6:]
        idlen = blockdata.find(" ")
        blockid = blockdata[:idlen]
        blockobj = json.loads(blockdata[idlen+1:])
        blocks[blockid] = block(blockobj)
    elif data.startswith("CLICK"):
        clickdata = data[6:]
        if clickdata.startswith(","):
            clickdata = clickdata[1:]

        if not(clickdata == "["):
            clickobj = json.loads(clickdata)
            clickedPID = pids[clickobj["name"]]
            clicks[clickobj["name"]] = clickobj
            try:
                os.kill(clickedPID, signal.SIGUSR1)
            except ProcessLookupError:
                print("Process likely ended... wait for the timeout")

    elif data.startswith("GETCLICK"):
        ID = data[9:]
        if ID in clicks:
            cs.send(bytes(json.dumps(clicks[ID]), "UTF-8"))
            del clicks[ID]
        else:
            cs.send(b"")

    elif data.startswith("PID"):
        pidata = data[4:]
        pid, ID = pidata.split(",")
        pids[ID] = int(pid)
