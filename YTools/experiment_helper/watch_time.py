import time

starttime = time.time()

def my_clock():
	'''调用time.time()来查看当前运行时间。比time.clock()准确
	'''
	return time.time() - starttime

__all__ = [my_clock]
