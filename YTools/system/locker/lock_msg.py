from ...network.communicate import SendServer , ListenServer , randport
from ...network.protocol import Protocol
from ...network.protocol import bytes2str , str2bytes , bytes2int , int2bytes , bytes2ip , ip2bytes
from subprocess import run as process_run
import pickle
import time
import sys

class Message:

	# 协议
	proto = Protocol(
		head = [
			["id" 		, 4 , int2bytes , bytes2int ] , 
			["type" 	, 4 , int2bytes , bytes2int ] , 
			["src_ip" 	, 4 , ip2bytes 	, bytes2ip  ] , 
			["src_port" , 4 , int2bytes , bytes2int ] , 
			["keylen" 	, 4 , int2bytes , bytes2int ] , 
			["vallen" 	, 4 , int2bytes , bytes2int ] , 
		] , 
		body = [
			["key" 		, "keylen" , str2bytes , bytes2str] , 
			["value" 	, "vallen" , pickle.dumps , pickle.loads] , 
		],
	)

	def __init__(self , type = "lock" , key = None , value = "", src_ip = None , src_port = None , id = -1 , data = None):
		'''type : set / ask / response

		set 将对应位置设为任意值
		ask 询问对应位置

		response 是应答值
		'''
		self.type2int = {
			"set" 		: 0,
			"unset"		: 1,
			"set_if" 	: 2,
			"ask" 		: 3,
			"response" 	: 4,
			"plus" 		: 5,
			"ask_pref" 	: 6,
		}
		self.int2type = ["set" , "unset" , "set_if" , "ask" , "response" , "plus" , "ask_pref"]

		if data is not None: # to decode
			self.__dict__.update(self.decode(data))
		else:
			self.data = self.encode(type , key , value , src_ip , src_port , id)

	def encode(self , type , key , value , src_ip , src_port , id):
		type = self.type2int[type]
		return self.proto.encode(type = type, key = key , value = value , src_ip = src_ip , src_port = src_port , id = id)
	def decode(self , data):
		ret = self.proto.decode(data)
		ret["type"] = self.int2type[ret["type"]]
		return ret
