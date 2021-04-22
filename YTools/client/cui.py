from ..universe.beautiful_str import beautiful_str , merge_str
import os

def processer_quit(ui , cmd):
	ui.closed = True
def processer_addenv(ui , cmd):
	ui.env[cmd[1]] = cmd[2]
def processer_delenv(ui , cmd):
	ui.env.pop(cmd[1])

class CUI:
	def __init__(self , processers = [ 
			["q"   , processer_quit   , "quit"] , 
			["add" , processer_addenv , "add a variable"] , 
			["del" , processer_delenv , "delete a variable"] , 
		]):
		self.closed = False
		self.processers = {}
		for name , func , info in processers:
			self.add_processor(name , func , info) 

		self.env = {} # 用来记录中间变量

		# 记录最近一次的命令
		self.original_command = "" 	# 原始命令
		self.cmd = [] 				# 分词之后的命令
		self.cmd_var = {} 			# 解释之后的命令

		# 记录以往的所有输入和输出
		self.buffer = []

		# 记录预先处理的input
		self.pre_comms = []

	def buf(self , x):
		x = str(x)
		self.buffer.append(x)
		self.buffer = self.buffer[-1000:]


	def output(self , x = ""):
		'''输出一行'''
		self.buf(x)
		print (x)
	def input(self , x = ""):
		'''输入一行'''
		if len(self.pre_comms) > 0:
			inp = self.pre_comms.pop(0)
		else:
			inp = input(x)

		self.buf(x + inp)
		return inp

	def add_processor(self , name , func , info = ""):
		'''添加一个处理方法'''
		self.processers[name] = [ func , info ]

	def get_command(self):
		'''获取一行命令'''
		self.command = self.input(">> ")
		return self.command

	def warn(self , text = ""):
		'''输出警告'''
		self.output ("WARN: {text}".format(text = text))

	def interpret_cmd(self , cmd , names , types = None , update_env = False):
		'''根据给定的name和type，把cmd的list转成dict'''
		if len(cmd) < len(names):
			self.warn("Number of arguments is wrong")
			return
		assert types is None or len(types) >= len(names)

		var = {names[i] : types[i](cmd[i]) if types is not None else cmd[i] for i in range(len(names))}
		self.cmd_var = var
		if update_env:
			self.env.update(var)
		return var

	def get_env_str(self):
		return beautiful_str(
			["Var Name" , "Var Val"] , 
			[[name , val] for name , val in self.env.items()]
		).strip()

	def get_info_str(self):
		return beautiful_str(
			["Comm Name" , "Comm info"] , 
			[[name , info] for name , (_ , info) in self.processers.items()]
		).strip()

	def flush(self):
		# 刷新行为
		os.system("cls")
		env_str = self.get_env_str()
		info_str = self.get_info_str()
		op_str = merge_str(env_str , info_str , ensured_length = True)
		print ("\n".join(self.buffer)) #把最近的记录一起输出
		print (op_str)

	def run(self):
		while not self.closed:
			self.flush()

			cmd = self.get_command().strip()
			cmd = cmd.split(" ")

			if len(cmd) <= 0:
				continue

			self.cmd = cmd


			p = self.processers.get(cmd[0])
			if p is None:
				self.warn("No processer of {name}".format(name = cmd[0]))
			else:
				p[0](self , cmd) # p[0]: func

	def fake_input(self , comm):
		self.pre_comms.append(comm)