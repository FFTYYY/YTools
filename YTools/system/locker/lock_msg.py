from ...network.communicate import SendServer , ListenServer , randport
from ...network.protocol import bytes2str , str2bytes , bytes2int , int2bytes , bytes2ip , ip2bytes
from subprocess import run as process_run
import time
import sys

class Message:
	def __init__(self , type = "lock" , key = None , value = "", src_ip = None , src_port = None , data = None , id = -1):
		'''type : set / ask / response

		set 将对应位置设为任意值
		ask 询问对应位置

		response 是应答值
		'''
		self.type2int = {
			"set" 		: 0,
			"ask" 		: 1,
			"response" 	: 2,
			"unset"		: 3,
		}
		self.int2type = ["set" , "ask" , "response" , "unset"]

		if data is not None: #解析消息
			self.data = data
			self.analyze()
		else: #构造消息
			self.type 		= type
			self.key 		= str(key)
			self.value 		= str(value)
			self.src_ip 	= str(src_ip)
			self.src_port 	= int(src_port)
			self.id = id

			head = self.make_head()
			self.data = head + str2bytes(self.key + self.value)

	def analyze(self):
		head , content 	= self.data[:24] , self.data[24:]

		type_num 		= bytes2int(head[:4])
		self.type 		= self.int2type[type_num]

		keylen_num		= bytes2int(head[4:8])
		value_num		= bytes2int(head[8:12])

		self.bad = False
		try:
			key_and_value 	= bytes2str(content)
		except UnicodeDecodeError:
			self.bad = True
			key_and_value = ""

		self.key 		= key_and_value[:keylen_num]
		self.value 		= key_and_value[keylen_num : keylen_num + value_num]

		self.src_ip 	= bytes2ip(head[12:16])
		self.src_port 	= bytes2int(head[16:20])
		self.id 		= bytes2int(head[20:24])

	def make_head(self):
		'''
			头部包含20个字节，前三个字节是3个int，分别是类型、key长度、值长度、源地址、源ip
		'''
		type_num 	= self.type2int[self.type]
		keylen_num 	= len(self.key)
		value_num 	= len(self.value)

		head = int2bytes(type_num) + int2bytes(keylen_num) + int2bytes(value_num) 
		head = head + ip2bytes(self.src_ip) + int2bytes(self.src_port)
		head = head + int2bytes(self.id)
		assert len(head) == 24

		return head
