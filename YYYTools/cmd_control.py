'''
	让同一个cmd执行多条命令（代替os.system())
	沙雕版
'''
import os
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import time

_mouse = PyMouse()
_key = PyKeyboard()

class Cmd:
	'''
		创建一个控制台对象，稍后可以对其提供指令
	'''
	def __init__(self , start_cmd_cm = ["start cmd"] , sleep_time = 0.3):
		'''
			创建一个控制台对象
			一条「指令」指的是一系列按键命令，由PyKeyboard来运行

			start_cmd_cm : 用于打开控制台的指令列表
			sleep_time : 每次执行指令的间隔时间（单位：秒）
				（因为指令实际上会并行执行，为了保证顺序执行，两个指令间要有一定的间隔）
		'''
		self.k = _key
		self.m = _mouse
		self.sleep_time = sleep_time
		self.start_cmd_cm = start_cmd_cm
		self.cm_lis = []

	def start(self):
		'''
			打开控制台，用初始化的时候提供的打开控制台指令
		'''
		for cm in self.start_cmd_cm:
			os.system(cm)
			time.sleep(0.1)

	def decide_func(self , cm):
		'''
			抉择对于一个指令应该用哪一个函数来运行之
		'''
		if isinstance(cm , str):
			if len(cm) > 1:
				return self.k.type_string
			return self.k.press_key
		elif isinstance(cm , list):
			return self.k.press_keys
		return self.k.press_key

	def add_cm(self , cm , sleep_time = -1):
		'''
			向指令列表中加入一条指令

			sleep_time : 运行完本次指令后的停留时间，如果给定的值<0或者留空则用默认值
		'''
		self.cm_lis.append( (cm , sleep_time) )

	def run_cm(self , cm , sleep_time = -1):
		'''
			立刻执行一条指令

			sleep_time : 运行完本次指令后的停留时间，如果给定的值<0或者留空则用默认值
		'''
		func = self.decide_func(cm)
		func(cm)

		if sleep_time < 0:
			time.sleep(self.sleep_time)
		else:
			time.sleep(sleep_time)

	def run(self , clear = False):
		'''
			按顺序运行指令列表

			clear: 是否在运行完后清空指令列表
		'''
		self.start()
		for x in self.cm_lis:
			self.run_cm(*x)
		if clear:
			self.clear()

	def clear(self):
		'''
			清空指令列表
		'''
		self.cm_lis = []

if __name__ == "__main__":
	cmd = Cmd()
	cmd.add_cm("python && python\n")
	cmd.add_cm("print ('hello')\n")
	cmd.run()