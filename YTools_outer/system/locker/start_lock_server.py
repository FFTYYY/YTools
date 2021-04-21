from YTools.network.communicate import SendServer , ListenServer , randport
from YTools.network.protocol import bytes2str , str2bytes , bytes2int , int2bytes , bytes2ip , ip2bytes
from multiprocessing import Process
import time
from YTools.system.locker.lock_msg import Message
from argparse import ArgumentParser
import os , sys
import signal
import threading

def acquire_updator(propers , inner_dict , key):
	# 先确保存在「修改者信号量」
	if propers["updator"].get(key) is None: 					#需要创建「修改者信号量」
		propers["creator"].acquire() 							#请求创建者信号量（锁住这个位置）
		if propers["updator"].get(key) is None: 				#我确实获取了本位置的创建者授权
			propers["updator"][key] = threading.Semaphore(1) 	#创建修改者信号量
		propers["creator"].release() 							#释放创建者
	
	#请求修改者授权
	propers["updator"][key].acquire() 							

def release_updator(propers , inner_dict , key):
	propers["updator"][key].release()

def set_a_val(inner_dict , key , val):
	ret_val = 1 #设置

	if val is None: # set to None 等同于删除
		ret_val = 3 #删除失败
		if inner_dict.get(key) is not None:
			inner_dict.pop(key)
			ret_val = 2 #成功删除
	else:
		inner_dict[key] = val

	return "" , ret_val

def locker_server_msg_callback(data , addr , who_get):

	propers  	= who_get.parent._p # 保存的所有参数
	inner_dict 	= propers["dict"] 	# 保存的那些值

	msg = Message(data = data) 		# 解析发过来的消息

	res_key = ""
	res_val = 1
	if msg.type == "set":
		acquire_updator(propers , inner_dict , msg.key)
		res_key , res_val = set_a_val(inner_dict , msg.key , msg.value)
		release_updator(propers , inner_dict , msg.key)

	if msg.type == "unset":
		acquire_updator(propers , inner_dict , msg.key)
		if inner_dict.get(msg.key) is not None:
			inner_dict.pop(msg.key)
		else:
			res_val = 0 #返回失败值
		release_updator(propers , inner_dict , msg.key)

	#如果值相等就设置值并返回1，否则返回0
	if msg.type == "set_if": 
		acquire_updator(propers , inner_dict , msg.key)
		expect_val , set_val = msg.value
		if inner_dict.get(msg.key) == expect_val:
			_ , _ = set_a_val(inner_dict , msg.key , set_val)
			res_val = 1
		else:
			res_val = 0 #失败值
		release_updator(propers , inner_dict , msg.key)
	
	#给某位置加一个值，返回加之后的值。用户自行保证值的存在和可加，locker模块只保证正确性
	if msg.type == "plus": 
		acquire_updator(propers , inner_dict , msg.key)
		res_val 			= inner_dict.get(msg.key) + msg.value
		inner_dict[msg.key] = res_val
		release_updator(propers , inner_dict , msg.key)

	if msg.type == "ask":
		res_val = inner_dict.get(msg.key)

	#查询所有满足这个前缀的key
	if msg.type == "ask_pref":
		res_val = [x for x in inner_dict if str(x).startswith(msg.key)]

	#查询所有满足这个前缀的key
	if msg.type == "clear":
		inner_dict.clear()


	# 返回消息
	ip 		= propers["ip"		]
	port 	= propers["port"	]
	sender 	= propers["sender"	]
	id 		= msg.id #向发送的那个id回信

	response = Message("response" , res_key , res_val , src_ip = ip , src_port = port , id = id)

	sender.add_target(msg.src_ip , msg.src_port)
	sender.send_to(msg.src_ip , msg.src_port , response.data)

def LockerServer(ip , port , patience):

	inner_dict = {}
	no_val_from = -1 # 上一次睡醒且没有任何值是多久

	sender = SendServer()
	listener = ListenServer(host = ip , port = port , callback = locker_server_msg_callback)
	propers = {} #通过这个dict来传递值
	propers["sender"] = sender
	propers["ip"	] = ip
	propers["port"	] = port
	propers["dict"	] = inner_dict

	propers["creator"] = threading.Semaphore(1) #目前只能有一个元素在新建属性
	propers["updator"] = {} 					#每个值同时只能有一个人在修改

	listener._p = propers
	listener.start()

	while True:
		if len(inner_dict) <= 0:
			if no_val_from < 0:
				no_val_from = time.time()
			else:
				if time.time() - no_val_from > patience:
					break
		else:
			no_val_from = -1
		time.sleep(patience) 
	
if __name__ == "__main__":

	print ("YLocker: 我活了！")

	args = ArgumentParser()
	args.add_argument("--ip" 		, default = "127.0.0.1" , type = str)
	args.add_argument("--port" 		, default = 34510 		, type = int)
	args.add_argument("--patience" 	, default = 10 			, type = int)
	args = args.parse_args()

	def exit(signu , frame):
		pass
	signal.signal(signal.SIGINT, exit) #防止父进程把CTRL+C传递到这里导致退出
	signal.signal(signal.SIGTERM, exit)

	LockerServer(args.ip , args.port , args.patience)