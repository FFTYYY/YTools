'''
	【TODO】需要改进之处 
	消息解析的性能
	安全性
'''

from ...network.communicate import SendServer , ListenServer , randport
from ...network.protocol import bytes2str , str2bytes , bytes2int , int2bytes , bytes2ip , ip2bytes
import time
import sys
from .lock_msg import Message
from .start_lock_server import run_this_module
from YTools.experiment_helper import Logger
import threading

class LockerClient:
	def __init__(self , server_ip = "127.0.0.1" , server_port = 34510 , listen_ip = "127.0.0.1" , patience = 2):
		self.server_ip = server_ip
		self.server_port = server_port

		self.lis_ip   = listen_ip
		self.lis_port = randport()
		self.listener = ListenServer(host = self.lis_ip , port = self.lis_port , callback = self.lis_callback)
		self.listener.start()

		self.try_to_connect()

		self.request_id = 0
		self.response_pool  = [None for _ in range(1024)] 					#循环使用的多个消息池，防止顺序问题
		self.seamahore_pool = [threading.Semaphore(0) for _ in range(1024)] #每个消息池收到消息，用信号量表示
		self.patience = patience

	def lis_callback(self , data , addr , who_get):
		msg = Message(data = data)
		self.response_pool[msg.id] = (msg.key , msg.value)
		self.seamahore_pool[msg.id].release()
		
	def try_to_connect(self):
		'''连接或启动server'''
		self.sender = SendServer()

		flag = False
		while not flag:
			flag = self.sender.add_target(self.server_ip , self.server_port)
			
			if not flag:
				run_this_module(args = [
					"--ip={0}".format(self.server_ip) , 
					"--port={0}".format(self.server_port) , 
				])

	def send_msg(self , msg):
		return self.sender.send(msg.data)

	def make_msg(self , type , key , val , id):
		return Message(type , key , val , src_ip = self.lis_ip , src_port = self.lis_port , id = id)

	def make_and_send(self , type , key , val , id):
		return self.send_msg(self.make_msg(type , key , val , id = id))

	def wait_retuen_val(self , func , *args , **kwargs):
		# 调用函数

		my_id = self.request_id #当前消息的id，期望回复也使用这个id
		self.request_id = (self.request_id + 1) % len(self.response_pool) #循环使用消息池
		self.response_pool[my_id] = None

		send_ret = func(*args , **kwargs , id = my_id)
		while len(send_ret) > 0:
			# print("连接失败")
			self.try_to_connect()
			send_ret = func(*args , **kwargs , id = my_id)

		# 等待返回值
		self.seamahore_pool[my_id].acquire(timeout = self.patience) #等待信号量

		while self.response_pool[my_id] is None: 	#如果实际上没有得到值（信号量超时）
			print ("未收到回复")
			self.try_to_connect() 					#重新建立连接
			func(*args , **kwargs , id = my_id) 	#重新发送
			self.seamahore_pool[my_id].acquire(timeout = self.patience) #重新等待信号量

		return self.response_pool[my_id]

	def ask_val(self , key):
		return self.wait_retuen_val(self.make_and_send , type = "ask" , key = key , val = "")

	def set_val(self , key , val):
		return self.wait_retuen_val(self.make_and_send , type = "set" , key = key , val = val)
		
	def unset_val(self , key):
		return self.wait_retuen_val(self.make_and_send , type = "unset" , key = key , val = "")
		
