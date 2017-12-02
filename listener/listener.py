import requests
import subprocess
from multiprocessing.connection import Listener


def listen():
    listener = Listener(('localhost', 6000), authkey=b'secret')
    conn = listener.accept()
    while True:
        msg = conn.recv()
        print("received: {}".format(msg))
        if msg == 'close':
            break

        if msg[0] == 'video':
            subprocess.Popen(['vlc', msg[1], '--fullscreen'])
        elif msg[0] == 'website':
            subprocess.Popen(['firefox', msg[1]])
        elif msg[0] == 'video-pause':
            requests.get('http://127.0.0.1:8080/requests/status.xml?command=pl_pause')
        elif msg[0] == 'video-stop':
            requests.get('http://127.0.0.1:8080/requests/status.xml?command=pl_stop')

listen()
