import math as M
from .strlen import max_len as real_len
def beautiful_str(name_list , value_list):
	'''输出一个很好看的表格。

	用法：
		beatiful_str(
			[title_1 , title_2 , ...] , 
			[
				[val_1_1 , val_1_2 , ... ] , 
				[val_2_1 , val_2_2 , ... ] , 
			]
		)

	示例：
		print (beautiful_str(
			["value_1" , "v2" , "value_3"] , 
			[
				[3.14156 , 2344 , 4.5678],
				[4,5,6],
				[123,"hahahaha" , 3456,],
			]
		))
	'''
	vn = len(name_list)

	len_list = list(name_list)
	for i in range(vn):
		len_list[i] = real_len(str(name_list[i]))
		for x in value_list:
			len_list[i] = max(len_list[i] , real_len(str(x[i])))
		len_list[i] += 2

	def get_imm(v):
		for i in range(vn):
			v[i] = str(v[i])

		the_str = "│"

		for i in range(vn):
			the_str += (" "*M.floor((len_list[i]-real_len(v[i]))/2))+v[i]+(" "*M.ceil((len_list[i]-real_len(v[i]))/2))
			the_str += "│"

		return the_str

	ceil , imm , floor = "┌" , "├" , "└"
	for i in range(vn):
		ceil  += ("─"*(len_list[i]//2))
		imm   += ("─"*(len_list[i]//2))
		floor += ("─"*(len_list[i]//2))
		if i != vn-1:
			ceil  += "┬"
			imm   += "┼"
			floor += "┴"
		else:
			ceil  += "┐"
			imm   += "┤"
			floor += "┘"

	title = get_imm(name_list)
	cont = ""
	for x in value_list:
		cont += get_imm(x) + "\n"

	return "\n" + ceil + "\n" + title + "\n" + imm + "\n" + cont + floor


def merge_str(s1 , s2 , inter = " " , ensured_length = False):
	'''
	给定两个带换行的字符串，把它们逐行合并
	TODO：自动判断字符串长度的方法有问题
	'''
	s1_line_len = real_len(s1) #s1每行的最长长度
	s1 , s2 = s1.split("\n") , s2.split("\n")
	s3 = ""
	for _i in range(max(len(s1),len(s2))):
		if not ensured_length:
			now_s = "" if _i >= len(s1) else s1[_i]
			now_s += " " * (s1_line_len - real_len(now_s))
		else:
			now_s = (" " * len(s1[0])) if _i >= len(s1) else s1[_i]

		if _i < len(s2): 
			now_s += inter + s2[_i]
		s3 += now_s + "\n"
	return s3

if __name__ == "__main__":
	print (beautiful_str.__doc__)
	print (beautiful_str(
		["value_1" , "v2" , "value_3"] , 
		[
			[3.14156 , 2344 , 4.5678],
			[4,5,6],
			[123,"hahahaha" , 3456,],
		]
	))

