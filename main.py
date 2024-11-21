import threading
from queue import Queue

queue = Queue()


def producer():
    for i in range(5):
        queue.put(i)
        print(f"Produced: {i}")


def consumer():
    while not queue.empty():
        item = queue.get()
        print(f"Consumed: {item}")


producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

producer_thread.start()
producer_thread.join()

consumer_thread.start()
consumer_thread.join()
