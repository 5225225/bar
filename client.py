import sys
import signal
import linelib


def handler(signum, frame):
    assert False


def rdclick():
    signal.setitimer(signal.ITIMER_REAL, 0.1)
    # Try to always update when the time is exactly on the second
    # This appears to be accurate to around 500u
    x = sys.stdin.readline()
    linelib.sendclick(x)
    signal.setitimer(signal.ITIMER_REAL, 0)


signal.signal(signal.SIGALRM, handler)
signal.signal(signal.SIGINT, signal.SIG_DFL)

sys.stdout.write('{"version": 1, "click_events": true}\n[\n')

while True:
    try:
        sys.stdout.write("{},\n".format(linelib.reqline().decode("UTF-8")))
    except ConnectionRefusedError:
        sys.stdout.write('[{"full_text": "start the server"}],\n')

    try:
        rdclick()
    except Exception:
        pass
