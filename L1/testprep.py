from threading import *
import time


# exemplu fara semafoare


# counter = 0


# def main(counter):
#     for i in range(5):
#         cnt = counter
#         counter = cnt+1
#     print(counter)
#     return counter


# t = Thread(target=main, args=(counter,))
# u = Thread(target=main, args=(counter,))

# t.start()
# u.start()


# exemplu cu semafor


# sem = Semaphore(1)
# n = 0


# def main2():
#     sem.acquire()
#     time.sleep(1)
#     global n
#     x = n
#     print("X= " + str(x))
#     n = x+1
#     print("N = " + str(n))
#     sem.release()
#     return n


# t1 = Thread(target=main2, args=())
# t2 = Thread(target=main2, args=())
# t3 = Thread(target=main2, args=())
# t4 = Thread(target=main2, args=())
# t5 = Thread(target=main2, args=())
# t6 = Thread(target=main2, args=())
# t7 = Thread(target=main2, args=())
# t8 = Thread(target=main2, args=())

# t1.start()
# t2.start()
# t3.start()
# t4.start()
# t5.start()
# t6.start()
# t7.start()
# t8.start()


# print(n)
