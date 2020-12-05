from .watch_time import my_clock
from ..universe.strlen import last_len
import time

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
	def __init__(self , mode = [print] , log_path = None , append = ["clock"] , line_length = 90):
		if log_path:
			self.log_fil = open(log_path , "w" , encoding = "utf-8")
		else:
			self.log_fil = None

		self.mode = mode

		if ("write" in mode) and (not log_path):
			raise Exception("Should have a log_path")

		self.append 	= append
		self.line_length = line_length

	def close(self):
		if self.log_fil:
			self.log_fil.close()

	def log(self , content = ""):

		content = self.pre_process(content)

		for x in self.mode:
			if x == "write":
				self.log_fil.write(content + "\n")
				self.log_fil.flush()
			else:
				x(str(content))

	def add_line(self , num = -1 , char = "-"):
		'''输出num个char , 如果num<0则默认line_length个
		'''
		if num < 0:
			num = self.line_length
		self.log(char * num)

	def pre_process(self , content):
		insert_space = self.line_length - last_len(content) #补全到line_length 
		content += " " * insert_space

		for x in self.append: #要往末尾添加哪些东西

			y = ""
			if x == "clock":
				y = "%.2fs" % (my_clock())
			elif x == "time":
				y = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime() )
			else:
				y = x()

			content += "| " + y + " "


		return content