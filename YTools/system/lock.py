from ..network.communicate import SendServer , ListenServer
from multiprocessing import Process
import time
# 自定义协议

class LockerServer(Process):
	def __init__(self , ip , port , patience = 10):
		'''
		超过patience秒没有锁，就自动结束
		'''
		self.locks = {}
		self.no_lock_from = -1

		self.listen = ListenServer(ip = ip , port = port , callback = self.get_msg_callback)

	def get_msg_callback(self , data , addr , who_get):
		print (data)

	def run(self):
		while True:
			if len(self.locks) <= 0:
				if self.no_lock_from < 0:
					self.no_lock_from = time.time()
				else:
					if time.time() - self.no_lock_from > self.patience:
						break

class Locker:
	def __init__(self , server_ip = "127.0.0.1" , server_port = 34510):
		self.server_ip = server_ip
		self.server_port = server_port

		self.try_to_connect()

	def try_to_connect(self):
		self.sender = SendServer()

		flag = False
		while flag:
			flag = self.sender.add_target(self.server_ip , self.server_port)
			if not flag:
				START_LOCK_SERVER # TODO : use subprocess，但是不能让子进程随着父进程关闭
