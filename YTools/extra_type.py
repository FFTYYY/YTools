class Struct:
	def __init__(self , *args , **kwargs):
		self._lis = args
		self._map = kwargs
		self.a = 12

	def __getattr__(self , name):
		if name == "_map":
			return self._map
		return self._map.get(name)

	def __getitem__(self , k):
		if isinstance(k , str):
			return self.__getattr__(k)

		try:
			k = int(k) % (len(self._lis))
		except Exception:
			return None
		return self._lis[k]
	
	def __unscroll__(self , name = True):
		if name:
			return self._map
		return self._lis
