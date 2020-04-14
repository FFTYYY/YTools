import pdb
from .beautiful_str import beautiful_str

class Struct:		
	'''一个可以自由添加元素的类。
	'''

	def __init__(self , **kwargs):
		self.__dict__ = kwargs

	def __get__(self , name):
		if name == "__dict__":
			return self.__dict__
		return self.__dict__.get(name)

	def __set__(self , name , val):
		self.__dict__[name] = val

	def __str__(self):
		return beautiful_str(["name" , "value"] , [[x , self.__dict__[x]] for x in self.__dict__])

