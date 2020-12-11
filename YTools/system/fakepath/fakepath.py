import os
import os.path as P 

my_path = P.abspath( P.dirname(__file__) )
fakep_name = "files/"
fakep_path = P.join(my_path , fakep_name)

def ensure_fakep():
	if not P.exists(fakep_path):
		os.makedirs(fakep_path , exist_ok = True)

def new_fakefolder(path):
	'''在伪路径中创建目录，返回创建好的目录的绝对路径'''
	ensure_fakep()

	path = P.join(fakep_path , path)
	os.makedirs(path , exist_ok = True)

	return P.abspath(path)

def fakepath_abs(path):
	'''给定伪路径，返回绝对路径'''
	ensure_fakep()
	return P.abspath( P.join(fakep_path , path) )
