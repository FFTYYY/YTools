import pdb
from .beautiful_str import beautiful_str

class Struct(object):		
	'''一个可以自由添加元素的类。
	'''

	def __init__(self , _default = None , **kwargs):
		self.__dict__.update(kwargs)
		self._default = _default
		self._getter = {}
		self._setter = {}

	def _set_property(self , name , getter , setter):
		self._getter[name] = getter
		self._setter[name] = setter

	def __getattr__(self , name):

		if name.startswith("_"):
			return object.__getattribute__(self , name)

		if hasattr(self , "_getter") and self._getter.get(name):
			return self._getter[name](self)

		if name not in self.__dict__:
			self.__dict__[name] = self._default

		return self.__dict__.get(name)

	def __setattr__(self , name , val):

		if hasattr(self , "_setter") and self._setter.get(name):
			self._setter[name](self , val)
			return 

		self.__dict__[name] = val

	def __str__(self):
		return beautiful_str(["name" , "value"] , [[x , self.__dict__[x]] for x in self.__dict__ if not x.startswith("_")])

