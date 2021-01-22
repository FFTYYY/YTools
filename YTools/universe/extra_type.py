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

SPECIAL = "_SPECIAL"

class Proxy:
	'''一个可以重写其他元素的类
	'''

	def __init__(self , original , specials):
		'''
		original：代理对象
		specials：代理属性


		访问一个Proxy对象时，如果属性在specials中，则会返回一个新版本，对于其他属性则都返回original的版本
		修改specials属性不影响original，其他属性则影响
		因此，可以重写specials属性，其他属性直接继承original
		'''
		self.__dict__["_special"]  = ["_original"] + specials
		self.__dict__["_original"] = original

	def __getattr__(self , name):
		if name == "_special" or name == "__dict__": #直接查询本对象
			return object.__getattribute__(self , name)

		if name in self._special: #直接查询本对象
			if name in self.__dict__:
				return self.__dict__[name]

		return getattr(self._original , name)

	def __setattr__(self , name , value):

		if name in self._special or name == "_special": #直接从dict设置本对象
			self.__dict__[name] = value
			return

		return setattr(self._original , name , value)
