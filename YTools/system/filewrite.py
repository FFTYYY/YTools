'''只要保证写的位置不重合，所有进程可以同时写文件！'''

def get_filesize(file):
	file.seek(0 , 2) #移到文件末尾
	return file.tell()

def write_file(file , pos , data , flush = True):
	file.seek(pos , 0) #从头偏移
	file.write(data)
	if flush:
		file.flush()
	return file

def read_file(file , pos , size):
	'''从pos开始读len个字节'''
	file.seek(pos , 0) #从头偏移
	return file.read(size)