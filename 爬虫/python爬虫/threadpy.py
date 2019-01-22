import threading
import random
import time
gmoney = 1000
lock = threading.Lock()
times = 0

class add(threading.Thread):

    def run(self):
        global gmoney
        global times
        while True:

            num = random.randint(100, 1000)
            lock.acquire()
            if times >= 10:
                lock.release()
                break

            gmoney += num
            lock.release()
            times += 1
            time.sleep(0.5)
            # print('add')
            print('现在有%d元'%gmoney)


class sole(threading.Thread):

    def run(self):
        global gmoney
        while True:
            num = random.randint(100, 1000)
            lock.acquire()
            if num > gmoney:
                print("钱不够发了还剩%d需要%d元" % (gmoney, num))
                #lock.release()

                if times >= 10:
                    lock.release()
                    break
            else:
                gmoney -= num
                lock.release()
                time.sleep(0.5)
                print('还剩%d元'%gmoney)
                # print('sole')


def main():
    t1 = add(name='印钱机')
    t2 = sole(name='女人')

    t1.start()
    t2.start()



if __name__ == '__main__':
        main()