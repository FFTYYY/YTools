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
	EMPTY_FLAG = "_EMPTY"

	def __init__(self):
		pass

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
		with FileLock(self.getfolder(key)): #锁定然后写入
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

	def _list_folders(self , folder):
		'''列出所目标子文件夹'''
		ret = []
		subfolers = os.listdir(folder)
		if self.VALFILE in subfolers: #存在值文件的是一个目标节点
			ret.append(folder)
		for p in subfolers:
			p = P.join(folder,p)
			if P.isdir(p):
				ret = ret + self._list_folders(p)
		return ret

	def ask_prefix(self , prefix , return_abs = False , only_suffix = False , not_none = False):
		'''查询所有key的前缀是给定prfix的key
		not_none：只返回非None的元素
		'''
		path = self.getfolder(prefix)
		ret = self._list_folders(path) #询问前缀下面的所有文件夹
		if not_none:
			ret = [x for x in ret if self.get(x) is not None]
		if return_abs:
			return ret
		if only_suffix:
			ret = [P.relpath(x , path) for x in ret] #求相对与前缀的相对路径
		else:
			the_path = self.getfolder("")
			ret = [P.relpath(x , the_path) for x in ret] #求伪路径
		return ret

	def clear(self):
		'''清除所有key'''
		all_dirs = self.ask_prefix("" , return_abs = True)
		for p in all_dirs:
			self.remove(p)

			if len( os.listdir(p) ) == 0: #为空才删除文件夹，否则就保留
				os.removedirs( p )
		self.clear_dir()
		return True

	def clear_dir(self , path = None):
		'''清除所有空文件夹'''
		if path is None:
			path = self.getfolder("")
		flag = True #自己是否能清除
		all_dirs = [P.join(path,p) for p in os.listdir(path) ]
		for p in all_dirs:
			if P.isdir(p):
				flag = flag and self.clear_dir(p)
			else:
				flag = False
		if flag: #现在应该已经没有文件了
			try:
				os.removedirs( path )
			except Exception:
				flag = False #不让删就算了
		return flag

