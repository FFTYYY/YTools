import random

def set_random_seed(seed , modules = ["random" , "torch" , "numpy"]):
	'''设置随机种子
		
	参数：
	seed：随机种子的值

	modules：要为哪些模块设置随机种子
		目前可选：random、torch、numpy
		注意torch中cuda也会被设置。
		只要gpu没问题，可以放心的使用。
	'''
	if "random" in modules:
		random.seed(seed)
	if "numpy" in modules:
		import numpy as np
		np.random.seed(seed)
	if "torch" in modules:
		import torch as tc
		import torch.backends.cudnn 
		tc.manual_seed(seed)
		tc.cuda.manual_seed_all(seed)
		torch.backends.cudnn.deterministic = True
		torch.backends.cudnn.benchmark = False
