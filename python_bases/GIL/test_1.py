import time
from threading import Thread
from multiprocessing import Process
from timeit import Timer

def countdown(n):
	while n > 0:
		n -= 1

def t1():
	COUNT = 100000000
	thread1 = Thread(target=countdown, args=(COUNT,))
	thread1.start()
	thread1.join()

def t2():
	COUNT = 100000000
	thread1 = Thread(target=countdown, args=(COUNT//2,))
	thread2 = Thread(target=countdown, args=(COUNT//2,))	
	thread1.start(), thread1.join()
	thread2.start(), thread2.join()

def t3():
	COUNT = 100000000
	p1 = Process(target=countdown, args=(COUNT//2,))
	p2 = Process(target=countdown, args=(COUNT//2,))
	p1.start(), p1.join()
	p2.start(), p2.join()

if __name__ == '__main__':
	t = Timer(t1)
	print 'countdown in one thread: ', t.timeit(1)
	t = Timer(t2)
	print 'countdown use two thread: ', t.timeit(1)
	t = Timer(t3)
	print 'countdown use two process: ', t.timeit(1)
		