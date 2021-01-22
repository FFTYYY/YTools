from ..universe.extra_type import Proxy

class FileIntercepter(Proxy):
	'''向原文件写的时候，同时向另一个地方写'''
	def __init__(self , original , write_other):
		super().__init__(original = original , specials = ["write" , "_write_other"])
		self._write_other = write_other

	def write(self , s):
		self._original.write(s)
		self._write_other(s)
