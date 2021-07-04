
_seed = 2333
def set_seed(val = 2333):
	global _seed
	_seed = val
def ask_seed():
	return _seed
def rand():
	val = (ask_seed() * 233) % 114514114514
	set_seed(val)
	return val