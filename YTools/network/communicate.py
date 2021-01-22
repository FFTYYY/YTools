import socket
import copy
import pdb
import threading
import random
from ..universe.onexit import add_quit_methods

MSG_MAX_LENGTH = 2048

def randport():
	return random.randint(23333 , 60000)

class SendServer:
	def __init__(self , host = "127.0.0.1"):
		self.host = host
		self.targets = {}

	def __del__(self):
		self.close()

	def add_target(self , ip = "127.0.0.1" , port = 65432):
		
		if self.targets.get( (ip , port) , None) is not None: #已经建立连接了
			return True

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			s.connect( (ip, port) )		
		except ConnectionRefusedError:
			return False

		self.targets[ip , port] = s

		return True

	def remove_target(self , ip , port):
		self.targets[ip , port].close()
		self.targets.pop((ip , port))

	def send(self , data):
		'''返回所有无法响应的目标'''

		leaved = []
		for ip , port in copy.copy(self.targets):
			if not self.send_to(ip , port , data):
				leaved.append((ip , port))
		return leaved

	def send_to(self , ip , port , data):
		'''return false if connection closed
		'''
		leaved = False

		try:
			self.targets[(ip , port)].sendall(data)
		except ConnectionResetError:
			leaved = True
			
		return not leaved

	def close(self):
		for addr , soc in self.targets.items():
			soc.close()


def default_callback(data , addr , who_get = None):
	ip , port = addr
	print (ip , ":" , port , " says ", data)

class ChildListener(threading.Thread):
	def __init__(self , conn , addr , callback , parent):
		threading.Thread.__init__(self)
		self.setDaemon(True)

		self.conn = conn
		self.addr = addr
		self.callback = callback
		self.closed = False
		self.parent = parent

		self.tarip = None
		self.tarport = None #listen port
		
	def __del__(self):
		self.close()

	def run(self):
		with self.conn:
			while not self.closed:
				try:
					data = self.conn.recv(MSG_MAX_LENGTH)
				except ConnectionResetError:
					if self.parent.unexpect_quit:
						self.parent.unexpect_quit(self.tarip , self.tarport)
					break

				if not data:
					continue
				self.callback(data , self.addr , who_get = self)
		self.close()

	def close(self):
		self.closed = True

class ListenServer(threading.Thread):
	def __init__(self , host  = "127.0.0.1" , port  = 65432 , callback = default_callback , block = False):
		threading.Thread.__init__(self)
		self.setDaemon(True)

		self.host = host
		self.port = port
		self.callback = callback

		self.childs = []
		self.closed = False
	
		self.block = block

		self.unexpect_quit = None

		add_quit_methods(self.close)

	def __del__(self):
		self.close()

	def run(self):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.bind((self.host, self.port))
			s.listen(50)

			while not self.closed:
				conn, addr = s.accept()

				new_child = ChildListener(conn , addr , self.callback , parent = self)
				new_child.start()
				self.childs.append(new_child)

	def close_one(self , tarip , tarport):
		the_child = None
		for x in self.childs:
			if x.tarip == tarip and x.tarport == tarport:
				the_child = x
				break
		if the_child is None:
			return

		the_child.close()
		self.childs.remove(the_child)

	def close(self):
		for x in self.childs:
			x.close()
		self.closed = True
