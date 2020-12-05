'''来自定义应用层协议吧！'''

def bytes2str(x):
	return str(x , encoding = "utf-8")

def str2bytes(x):
	return bytes(x , encoding = "utf-8")

def bytes2int(x):
	return int.from_bytes(x , byteorder = 'little')

def int2bytes(x , length = 4):
	return x.to_bytes(length , byteorder = 'little')

def int2ip(x):
	a = ((x & 0x000000FF) >> 0)
	b = ((x & 0x0000FF00) >> 8)
	c = ((x & 0x00FF0000) >> 16)
	d = ((x & 0xFF000000) >> 24)
	return "%d.%d.%d.%d" % (d,c,b,a)

def ip2int(x):
	d,c,b,a = [int(w) for w in x.strip().split(".")]
	return (d << 24) | (c << 16) | (b << 8) | (a << 0)

def bytes2ip(x):
	return int2ip(bytes2int(x))
	
def ip2bytes(x):
	return int2bytes(ip2int(x) , 4)

class DataReader:
	def __init__(self):
		self.reset()
	def reset(self):
		self._now_pos = 0
	def read(self , data , length):
		'''从给定数据中读取特定长度的数据，如果length=-1，则会读取剩下所有数据
		'''
		if length < 0:
			return data[self._now_pos : ]
		self._now_pos += length
		return data[self._now_pos - length : self._now_pos]
	def __call__(self , *pargs , **kwargs):
		return self.read(*pargs , **kwargs)
