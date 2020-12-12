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
	def __init__(self , data = None):
		self.data = data
		self.reset()

	def reset(self):
		self.now_pos = 0

	def read(self , length , data = None):
		'''从给定数据中读取特定长度的数据，如果length=-1，则会读取剩下所有数据
		'''
		if data is None:
			data = self.data

		if length < 0:
			return data[self.now_pos : ]

		self.now_pos += length
		return data[self.now_pos - length : self.now_pos]

	def __call__(self , *pargs , **kwargs):
		return self.read(*pargs , **kwargs)

class Protocol:
	def __init__(self , standard):
		'''
			协议标准：
			{
				"head": [
					[ 项目名 , 项目长度 , 编码方法 , 解码方法 ] ,
				] , 
				"body": [
					[ 项目名 , 项目长度 , 编码方法 , 解码方法 ] , 
				] , 
			}
			其中head的长度必须是固定的。body的项目长度可以是固定的，也可以是字符串，表示用长度为对应的head。
			body的最后一项也可以是-1，表示剩下所有数据

			例：
			standard = {
				"head": [
					["id"  , 4 , int2bytes , bytes2int] , 
					["len" , 4 , int2bytes , bytes2int] , 
				] , 
				"body": [
					["content" , "len" , str2bytes , bytes2str]
				]
			}
		'''

		self.standard = standard
		self.head = self.standard["head"]
		self.body = self.standard["body"]

		self.headsize = sum([x[1] for x in self.head])

	def encode_head(self , **kwargs):
		head = b''
		for name , length , encode_f , decode_f in self.head:
			encoded = encode_f(kwargs[name])

			if len(encoded) != length:
				raise "length incorrect"

			head += encoded
		return head

	def encode_body(self , **kwargs):
		body = b''
		for name , length , encode_f , decode_f in self.body:
			encoded = encode_f(kwargs[name])

			if isinstance(length , int):
				if len(encoded) != length:
					raise "length incorrect"
			else:
				if len(encoded) != kwargs[length]:
					raise "length incorrect"

			body += encoded

		return body

	def encode(self , **kwargs):
		return self.encode_head(**kwargs) + self.encode_body(**kwargs)

	def decode_head(self , head):

		decoded_head = {}

		data = DataReader(head)
		for name , length , encode_f , decode_f in self.head:
			encoded = data.read(length)
			decoded = decode_f(encoded)

			decoded_head[name] = decoded
		return decoded_head

	def decode_body(self , body , decoded_head):
		decoded_body = {}

		data = DataReader(body)
		for name , length , encode_f , decode_f in self.body:

			if isinstance(length , str):
				length = decoded_head[length]

			encoded = data.read(length)
			decoded = decode_f(encoded)

			decoded_body[name] = decoded
		return decoded_body


	def decode(self , encoded):
		head = encoded[:self.headsize]
		body = encoded[self.headsize:]

		decoded_head = self.decode_head(head)
		decoded_body = self.decode_body(body , decoded_head)

		decoded_body.update(decoded_head)

		return decoded_body
