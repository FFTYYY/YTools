import time
from YYYTools.beautiful_str import beautiful_str as tostr
from timeit import default_timer as gettime

class Timer:
	time_sum = {}
	count = {}
	before_enter = []
	before_exit = []

	def __init__(self , name):
		self.name = name

	def __enter__(self):
		for x in Timer.before_enter:
			x()
		self.start_time = gettime()
		return self

	def __exit__(self , *args , **kwargs):
		for x in Timer.before_exit:
			x()
		the_time = gettime() - self.start_time

		if self.time_sum.get(self.name) is None:
			self.time_sum[self.name] = 0
			self.count[self.name] = 0
		
		self.time_sum[self.name] += the_time
		self.count[self.name] += 1

	def get_time(name , average = False):
		if Timer.time_sum.get(name) is None:
			return "None"
		ret = Timer.time_sum[name]
		if average:
			ret /= Timer.count[name]
		return ret

	def get_avg_time(name):
		return Timer.get_time(name , True)

	def clear():
		Timer.time_sum = {}
		Timer.count = {}

	def get_all(average = False):
		time_sum = Timer.time_sum
		count = Timer.count

		ret = []
		for x in time_sum:
			if average:
				ret.append([x , time_sum[x] , count[x]])
			else:
				ret.append([x , time_sum[x] / count[x] , count[x]])

		return ret

	def output_all():
		def f2s(f):
			return "%.10f" % f
		time_sum = Timer.time_sum
		count = Timer.count
		ret = []
		for x in time_sum:
			ret.append([x , f2s(time_sum[x]) , count[x] , f2s(time_sum[x] / count[x])])

		return tostr(["name" , "time (s)" , "count" , "avg_time (s)"]  , ret)

if __name__ == "__main__":

	Timer.before_enter.append(lambda : print ("now start"))

	with Timer("hahah"):
		print (123)

	with Timer("fuck"):
		time.sleep(1)
	with Timer("fuck"):
		time.sleep(1)
	with Timer("fuck"):
		time.sleep(1)

	print(Timer.output_all())

