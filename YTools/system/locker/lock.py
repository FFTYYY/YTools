import time
import sys
import pickle
from ..fakepath import new_fakefolder , fakepath_abs
from .filelock import FileLock
import os.path as P
import os
class LockerClient:

	NAME = "YLocker"
	VALFILE = "val.pkl"

	def __init__(self):
		self.fakepath = new_fakefolder(self.NAME)

	def getfolder(self , foldername):
		# 给定目录名，返回其绝对路径
		return new_fakefolder(P.join(self.NAME , foldername))

	def ensurefile(self , foldername):
		# 给定目录名，返回值文件的绝对路径
		filename = self.VALFILE
		path = P.join(self.getfolder(foldername) , filename)
		open(path , "ab").close()
		return path

	def encode(self , val):
		return pickle.dumps(val)
	def decode(self , content):
		if len(content) == 0:
			return None
		return pickle.loads(content)

	def get(self , key):
		path = self.ensurefile(key)
		with open(path , "rb") as fil:
			content = fil.read()
		return self.decode(content)

	def set(self , key , val):
		path = self.ensurefile(key)
		with FileLock(self.getfolder(key)): #锁定然后写入
			with open(path , "wb") as fil:
				fil.write(self.encode(val))
		return True
		
	def remove(self , key):
		path = self.ensurefile(key)
		with FileLock(self.getfolder(key)): #锁定然后删除文件
			os.remove(path)
		return True
	
	def plus(self , key , val = 1):
		'''同步加一，返回加后的值'''		
		path = self.ensurefile(key)
		with FileLock(self.getfolder(key)): #锁定然后加一
			with open(path , "rb") as fil:
				store_val = self.decode(fil.read())
			store_val = store_val + val
			with open(path , "wb") as fil:
				fil.write(self.encode(store_val))

		return store_val
		
	def set_if(self , key , expect_val , set_val):
		'''如果当前值 = expect_val，则设为set_val'''
		path = self.ensurefile(key)
		with FileLock(self.getfolder(key)):
			with open(path , "rb") as fil:
				store_val = self.decode(fil.read())
			if store_val == expect_val:
				with open(path , "wb") as fil:
					fil.write(self.encode(set_val))

		return True

	def ask_prefix(self , prefix):
		'''查询所有key的前缀是给定prfix的key'''
		
		all_dirs = os.listdir(self.fakepath)
		return [ p for p in all_dirs if P.isdir(p) and p.startswith(prefix) ]

	def clear(self):
		'''清除所有key'''
		all_dirs = self.ask_prefix("")
		for p in all_dirs:
			os.removedirs( p )
		return True 