import os

class TempCWD:
	'''临时CWD。

	用法：
	with TempCWD(path):
		do_someting

	然后这个do_something会被视为在path下运行，不会影响原始环境的cwd
	'''

	def __init__(self , temp_path):
		self.temp_path = temp_path

	def __enter__(self):
		self.old_cwd = os.getcwd()
		os.chdir(self.temp_path)
		return self

	def __exit__(self , *args , **kwargs):
		os.chdir(self.old_cwd)


