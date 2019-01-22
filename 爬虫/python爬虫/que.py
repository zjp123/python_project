from queue import Queue
import threading
import time


class TT(threading.Thread):

    def __init__(self, que, *args, **kwargs):
        super(TT, self).__init__(*args, **kwargs)
        self.que = que
        #print(99)

    def run(self):

        while True:
            if self.que.empty():
                break
            else:
                print(self.que.get())
                time.sleep(1)


def main():

    q = Queue(8)
    for x in range(8):
        q.put(x)

    for x in range(5):
        t = TT(q)
        t.start()
   # print(00)


if __name__ == '__main__':
    main()