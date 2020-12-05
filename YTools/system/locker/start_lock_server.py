from ...network.communicate import SendServer , ListenServer , randport
from ...network.protocol import bytes2str , str2bytes , bytes2int , int2bytes , bytes2ip , ip2bytes
from multiprocessing import Process
import time
from .lock_msg import Message
from argparse import ArgumentParser
from subprocess import Popen
import os , sys
import signal
from YTools.universe.timer import Timer
from YTools.experiment_helper.logger import Logger

def run_this_module(args = []):
	Popen(args = [sys.executable , "-m" , __name__] + args)

def locker_server_msg_callback(data , addr , who_get):

	who_get = who_get.parent
	locks = who_get._m_locks

	msg = Message(data = data)

	if not msg.bad:
		if msg.type == "set":
			locks[msg.key] = msg.value
		
		if msg.type == "unset":
			if locks.get(msg.key , None) is not None:
				res_val = locks.pop(msg.key)
			else:
				res_val = None
		else:
			res_val = str(locks.get(msg.key))
		res_key = msg.key
	else:
		res_key = "bad"
		res_val = "bad"

	# 返回消息
	ip 		= who_get._m_ip
	port 	= who_get._m_port
	sender 	= who_get._m_sender
	id 		= msg.id #向发送的那个id回信

	response = Message("response" , res_key , res_val , src_ip = ip , src_port = port , id = id)

	sender.add_target(msg.src_ip , msg.src_port)
	sender.send_to(msg.src_ip , msg.src_port , response.data)

def LockerServer(ip , port , patience):

	locks = {}
	no_lock_from = -1

	sender = SendServer()
	listener = ListenServer(host = ip , port = port , callback = locker_server_msg_callback)
	listener._m_sender 	= sender
	listener._m_ip 		= ip
	listener._m_port 	= port
	listener._m_locks 	= locks
	listener.start()

	while True:
		if len(locks) <= 0:
			if no_lock_from < 0:
				no_lock_from = time.time()
			else:
				if time.time() - no_lock_from > patience:
					break
		time.sleep(2)
	
if __name__ == "__main__":

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