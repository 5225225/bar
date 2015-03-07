import socket
import json
import os
import signal


def getclick(ID):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 1337))
    s.send(bytes("GETCLICK {}".format(ID), "UTF-8"))
    clickobj = s.recv(2048)
    s.close()
    return clickobj


def waitsig(seconds):
    signal.alarm(int(seconds))
    signal.pause()


def sendclick(x):
    # NOT TO BE USED BY MODULES
    # Only the client needs to use this.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 1337))
    s.send(bytes("CLICK {}".format(x.strip()), "UTF-8"))
    s.close()


def sendPID(ID):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("localhost", 1337))
        s.send(bytes("PID {},{}".format(os.getpid(), ID), "UTF-8"))
    except InterruptedError:
        pass

    s.close()


def reqline():
    # you are expected to handle connectionrefusederrors yourself
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 1337))
    s.send(b"LINE")
    return s.recv(2048)
    s.close()


def sendblock(blockid, obj):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("localhost", 1337))
        s.send(bytes("BLOCK {} {}".format(blockid, json.dumps(obj)), "UTF-8"))
    except InterruptedError:
        # This is very rare, and really only happens if you try to make it
        # crash by scrolling a lot on a block. Still, the program shouldn't
        # crash. It's okay to just skip the update this time, it'll get
        # updated on the next go
        pass


def sendmultiblock(blockid, blocks):
    for index, obj in enumerate(blocks):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 1337))
        if not index == len(blocks)-1:
            obj["separator"] = False
            obj["separator_block_width"] = 0
        s.send(bytes("BLOCK {} {}".format(blockid + str(index),
                                          json.dumps(obj)),
                     "UTF-8"))
