from .watch_time import my_clock
from ..universe.strlen import last_len
import time
from typing import Union

class Logger:
	'''自动日志。

	参数：
	mode：一个函数，代表输出方向。"write"表示向文件写
	log_path：日志文件的位置。如果选了"write"的话必须填此项。如果打开了文件最后一定要调用close()
	append：往末尾添加哪些信息。clock表示当前运行秒数，time表示当前时间，也可以用其他函数


	方法：
	log：输出一个字符串
	close：关闭文件
	
	'''
	def __init__(self , mode = [print] , log_path = None ,  extra = ["clock"]):
		if log_path:
			self.log_fil = open(log_path , "w" , encoding = "utf-8")
		else:
			self.log_fil = None

		self.mode = mode

		if ("write" in mode) and (not log_path):
			raise Exception("Should have a log_path")

		self.extra 	= extra

	def close(self):
		if self.log_fil:
			self.log_fil.close()

	def log(self , content: str = ""):

		if isinstance(content , str):

			content = self.pre_process(content)

			for md in self.mode:
				if md == "write" and self.log_fil:
					self.log_fil.write(content + "\n")
					self.log_fil.flush()
				else:
					md(str(content))

	def add_line(self , num: int = 90 , char: str = "-"):
		'''输出num个char , 如果num<0则默认line_length个
		'''
		self.log(char * num)

	def pre_process(self , content):

		for ex in self.extra: #要往开头添加哪些东西

			to_add = ""

			if ex == "clock":
				to_add = "%.2fs" % (my_clock())
			elif ex == "time":
				to_add = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime() )
			else:
				to_add = ex()

			content = f"[{to_add}] {content}"


		return content
	
