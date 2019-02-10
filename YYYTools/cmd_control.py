'''
	让同一个cmd执行多条命令（代替os.system())
	沙雕版
'''

from pymouse import PyMouse
from pykeyboard import PyKeyboard
import time

_mouse = PyMouse()
_key = PyKeyboard()

class Cmd:
	def __init__(self , start_cmd_cm =[[_key.windows_l_key , "r"] , "cmd\n"] , sleep_time = 0.3):
		self.k = _key
		self.m = _mouse
		self.sleep_time = 0.3
		self.start_cmd_cm = start_cmd_cm
		self.cm_lis = []

	def start(self):
		for cm in self.start_cmd_cm:
			self.run_cm(cm)

	def decide_func(self , cm):
		if isinstance(cm , str):
			if len(cm) > 1:
				return self.k.type_string
			return self.k.press_key
		elif isinstance(cm , list):
			return self.k.press_keys
		return self.k.press_key

	def add_cm(self , cm , sleep_time = -1):
		self.cm_lis.append( (cm , sleep_time) )

	def run_cm(self , cm , sleep_time = -1):
		func = self.decide_func(cm)
		func(cm)

		if sleep_time < 0:
			time.sleep(self.sleep_time)
		else:
			time.sleep(sleep_time)

	def run(self):
		self.start()
		for x in self.cm_lis:
			self.run_cm(*x)

if __name__ == "__main__":
	cmd = Cmd()
	cmd.add_cm("python\n")
	cmd.add_cm("print ('hello')\n")
	cmd.run()