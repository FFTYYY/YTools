'''
	一个用来调试带有递归代码的工具
	可以显示递归逻辑、查找节点和查看节点的一些值
	
	其中Node表示节点，由Debuger创建
	RecursionDebuger是主工具，应为每一个需要调试的函数创建一个该类对象
'''

import re

class Node:
	'''
			father是一个Node，表示节点的父节点，为None则说明此节点为根节点
			name是一个元组，表示节点的名字，应是一个元组
			dic是一个字典，表示这个节点的可查询值列表
			son是一个字典，表示所有节点的名字和对应的节点
	'''
	def __init__(self , father = None , name = None , dic = {} , name_in_fat = None , name_in_all = None):
		'''
			father表示节点的父节点，为None则说明此节点为根节点
			name表示节点的名字，应是一个元组
			dic表示这个节点的可查询值列表
		'''
		self.father = father
		self.sons = {}
		self.name = name
		self.name_in_fat = name_in_fat
		self.name_in_all = name_in_all
		self.dic = dic

	def is_root(self):
		return self.father == None

	def ask_sons(self,p):
		'''
			查询所有名字为p的儿子列表
			返回值第一个元素是儿子节点对象，第二个元素是这个儿子在父亲下的名字
		'''
		ret = []
		if(self.sons.get(p)):
			ret.append( self.sons[p] )

		now_num = 0
		while True:
			the_tuple = (p , now_num)
			if(self.sons.get(the_tuple)):
				ret.append( self.sons[the_tuple] )
			else:
				break
			now_num += 1
		return ret

	def add_son(self,node):
		name = node.name
		if(self.sons.get(name) != None):
			name = (name,0)
		while(self.sons.get(name) != None):
			name = (name[0],name[1] + 1)
		self.sons[name] = node
		return name

class RecursionDebuger_CUI:
	def __init__(self,parent):
		self.parent = parent
		self.now_node = parent.root

	def get_node_name_info(self,node):

		fat_nam = "root"
		if(node.father != None):
			fat_nam = node.father.name_in_all
		return "{0} ，父亲为：{1} ，父中名为：{2}，全局名为：{3}".format(
				node.name , 
				fat_nam , 
				node.name_in_fat , 
				node.name_in_all 
			)

	def print_node(self,node,start_info = "" , end_info = ""):

		print ()
		print (start_info)
		print ("------------")

		print("当前节点 " + self.get_node_name_info(node) + "，信息列表：")

		for ite in node.dic:
			print ("\t" + str(ite) + " : " + str(node.dic[ite]))

		print ("------------")
		print (end_info)
		print ()

	def go_into_son(self,node,start_info = "" , end_info = ""):

		print ()
		print (start_info)
		print ("------------")

		name = input("输入儿子的名：")
		name = re.split("," , name)
		for i in range(len(name)):
			name[i] = int(re.sub("\D" , "" , name[i]))
		name = tuple(name)

		ret = node.ask_sons(name)
		while(len(ret) == 0):
			print ("儿子不存在，重新输入...")
			name = input("输入儿子的名：")
			if(len(name) == 0):
				print ("退出输入...")
				return 
			name = re.split("," , name)
			for i in range(len(name)):
				name[i] = int(re.sub("\D" , "" , name[i]))
			name = tuple(name)
			ret = node.ask_sons(name)

		node_num = -1
		if(len(ret) == 1):
			node_num = 0
		elif(len(ret) > 1):
			print("有若干匹配的节点，输入编号来指定具体某一个：")

			_cnt = 0
			for the_son in ret:
				print("{0} : {1}".format(_cnt , self.get_node_name_info(the_son)))
				_cnt += 1

			node_num = -1
			while(node_num < 0 or node_num >= len(ret)):
				node_num = int(input("输入编号："))

		self.now_node = ret[node_num]

		print("已进入。节点名:{0}".format(self.now_node.name))

		print ("------------")
		print (end_info)
		print ()

	def look_sons(self,node,start_info = "" , end_info = ""):

		print ()
		print (start_info)
		print ("------------")

		print ("当前节点 {0} 儿子列表：".format(node.name))

		for nam in node.sons:
			print ("\t" + str(nam))

		print ("------------")
		print (end_info)
		print ()

	def goto_father(self,node,start_info = "" , end_info = ""):

		print ()
		print (start_info)
		print ("------------")

		self.now_node = self.now_node.father

		print("完成。")
		print("当前节点名:{0}".format(self.now_node.name))

		print ("------------")
		print (end_info)
		print ()


	def exec_(self):

		self.now_node = self.parent.root

		commad_list = {
			"当前节点" 		: 0,
			"0" 			: 0,
			"info" 			: 0,

			"进入儿子" 		: 1,
			"1" 			: 1,
			"down" 			: 1,

			"查看儿子" 		: 2,
			"2" 			: 2,
			"son" 			: 2,

			"查找名字" 		: 3,
			"3" 			: 3,
			"search" 		: 3,

			"进入父亲" 		: 4,
			"4" 			: 4,
			"up" 			: 4,

		}

		while(True):

			print()
			cm = input("输入指令：")
			while(commad_list.get(cm) == None):
				print ("指令 \"{0}\" 不在指令列表中。".format(repr(cm)))
				print (cm)
				cm = input("输入指令：")

			cm = commad_list[cm]

			if(cm == 0):
				self.print_node(self.now_node)
			elif(cm == 1):
				self.go_into_son(self.now_node)
			elif(cm == 2):
				self.look_sons(self.now_node)
			elif(cm == 3):
				self.go_into_son(self.parent.all)
			elif(cm == 4):
				self.goto_father(self.now_node)

class RecursionDebuger:

	def __init__(self):
		'''
			·在递归过程的开始调用set_point()以创建节点，并给定一个元组作为节点名
				（可以重名，若如此会被加入额外的编号作为命名（比如(a,b)会被改为((a,b),0)））

			·在递归结束时调用end_point()以结束创建节点，并给定一个dict作为可查找变量列表

			在递归完整结束后，可以通过这个工具来查看所记录的信息
		'''
		self.stack = []
		self.root = None
		self.now_info = {}
		self.all = Node()


	@property
	def cui(self):
		'''
			创建本调试器的命令行界面
			需要在信息获取完全后创建
		'''
		return RecursionDebuger_CUI(self)

	def set_point(self,name):
		'''
			创建节点
			name表示将要创建的节点的名字
		'''
		fat = None
		if(len(self.stack) > 0):
			fat = self.stack[-1]

		new_node = Node(father = fat , name = name , dic = {})

		if(fat):
			the_name = fat.add_son(new_node)
			new_node.name_in_fat = the_name
		else:
			self.root = new_node

		the_name = self.all.add_son(new_node)
		new_node.name_in_all = the_name

		self.stack.append(new_node)

	def add_info(self,info_name,info_val):
		#TODO : BUG!!!!
		self.now_info[info_name] = info_val

	def end_point(self,dic = {}):

		if(len(self.stack) <= 0):
			raise Exception("RecursionDebuger.end_pont() : bad call")

		the_las = self.stack.pop()

		self.now_info.update(dic)
		the_las.dic = self.now_info
		self.now_info = {}


