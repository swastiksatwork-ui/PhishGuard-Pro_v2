import sys
import time
import random
from threading import Thread
from queue import Queue

socketio = None

# Queue storing chunks waiting to be shown
terminal_queue = Queue()

# Number of characters per browser update
CHUNK_SIZE = 200


class StreamToBrowser:

    def __init__(self, original_stream):
        self.original_stream = original_stream

    def write(self, message):

        # Keep VS Code terminal instant
        self.original_stream.write(message)
        self.original_stream.flush()

        if not message:
            return

        # Split into fixed-size chunks
        start = 0

        while start < len(message):

            chunk = message[start:start + CHUNK_SIZE]

            if chunk:
                terminal_queue.put(chunk)

            start += CHUNK_SIZE

    def flush(self):
        self.original_stream.flush()


def browser_sender():

    while True:

        chunk = terminal_queue.get()

        qsize = terminal_queue.qsize()

        # Adaptive delay
        if qsize <= 10:
            delay = random.uniform(10, 12)

        elif qsize <= 25:
            delay = random.uniform(8, 10)

        elif qsize <= 50:
            delay = random.uniform(6, 9)

        elif qsize <= 100:
            delay = random.uniform(3, 5)

        elif qsize <= 250:
            delay = random.uniform(1.8, 2.9)

        else:
            delay = random.uniform(1.3, 1.7)

        time.sleep(delay)

        if socketio:
            socketio.emit(
                "terminal",
                {
                    "line": chunk
                }
            )

        terminal_queue.task_done()


def init_terminal_stream(sio):

    global socketio

    socketio = sio

    sys.stdout = StreamToBrowser(sys.stdout)
    sys.stderr = StreamToBrowser(sys.stderr)

    Thread(
        target=browser_sender,
        daemon=True
    ).start()