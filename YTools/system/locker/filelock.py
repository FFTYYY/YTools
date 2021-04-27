'''注意，这个模块可能死锁'''

from ..fakepath import fakepath_abs , new_fakefolder
import os
import random
import os.path as P

my_id = "{pid}_{seed}".format( pid = os.getpid() , seed = random.randint(0,233333)) #进程相关的id
name = "YFILELOCK/"
new_fakefolder(name)

def get_path(foldername):
	'''给定lock的文件夹名，创建对应文件夹'''
	pt = fakepath_abs(P.join(name , foldername))
	new_fakefolder(pt)
	return pt

def checkfile(path , my_filename):
	'''参数是绝对路径，检查这个路径下面有没有.lock结尾的文件，返回True表示没有。'''
	return len( [ x for x in os.listdir(path) if x.endswith(".lock") and x != my_filename] ) == 0


def acquire_lock(foldername , my_name = "0"):
	my_filename = "{my_id}_{my_name}.lock".format(my_id = my_id , my_name = my_name) #生成自己的锁文件的文件名
	path = get_path(foldername) #锁目录
	my_file = P.join(path , my_filename) #自己的锁文件的文件路径

	while True:	
		# 等待其他进程释放锁
		while not checkfile(path , my_filename): pass

		# 上自己的锁
		open(my_file , "w").close()

		if not checkfile(path , my_filename): # 如果发现还有不是自己的锁
			os.remove(my_file)  # 就删掉自己的锁
			continue 			# 并重新检查

		break # 加锁成功

def release_lock(foldername , my_name = "0"):
	my_filename = "{my_id}_{my_name}.lock".format(my_id = my_id , my_name = my_name) #生成自己的锁文件的文件名
	path = get_path(foldername) #锁目录
	my_file = P.join(path , my_filename) #自己的锁文件的文件名
	os.remove(my_file)  # 删掉自己的锁



class FileLock:
	'''锁定一个文件（目录）'''

	def __init__(self , foldername , threadname = None):
		if threadname is None:
			threadname = str( random.randint(0,233333) ) #生成一个线程相关的随机数

		self.foldername = foldername
		self.threadname = threadname

	def __enter__(self):
		acquire_lock(self.foldername , self.threadname)
		return self

	def __exit__(self , *args , **kwargs):
		release_lock(self.foldername , self.threadname)


