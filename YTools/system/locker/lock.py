'''
	【TODO】需要改进之处 
	消息解析的性能
	安全性
'''

import time
import sys
import threading
from subprocess import Popen

class LockerClient:


	def __init__(self):
		pass
	def get(self , key):
		return self.wait_return_val(self.make_and_send , type = "ask" , key = key , val = None)

	def set(self , key , val):
		return self.wait_return_val(self.make_and_send , type = "set" , key = key , val = val)
		
	def remove(self , key):
		return self.wait_return_val(self.make_and_send , type = "unset" , key = key , val = None)
	
	def plus(self , key , val):
		return self.wait_return_val(self.make_and_send , type = "plus" , key = key , val = val)
		
	def set_if(self , key , expect_val , set_val):
		'''如果当前值 = expect_val，则设为set_val'''
		return self.wait_return_val(self.make_and_send , type = "set_if" , key = key , val = [expect_val , set_val])

	def ask_prefix(self , prefix):
		'''查询所有key的前缀是给定prfix的key'''
		return self.wait_return_val(self.make_and_send , type = "ask_pref" , key = prefix , val = None)

	def clear(self):
		'''清除所有key'''
		return self.wait_return_val(self.make_and_send , type = "clear" , key = "" , val = None)
