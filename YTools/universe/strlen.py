'''求字符串的显示长度'''

def len_ignore_n(s):
	'''无视\n的s的长度
	'''
	s = str(s).strip()
	s = s.replace("\n" , "")

	l = (len(bytes(s , encoding = "utf-8")) - len(s)) // 2 + len(s) #中文
	l += 7 * s.count("\t")											#\t

	return l

def max_len(s):
	'''每行最大长度
	'''
	s = str(s).strip()
	return max([len_ignore_n(x) for x in s.split("\n")])

def last_len(s):
	'''最后一行的长度
	'''
	s = str(s).strip()
	return len_ignore_n(s.split("\n")[-1])