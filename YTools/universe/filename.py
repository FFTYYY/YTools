import random
import pickle

def random_name(lenmax = 8):
	g1 = "aeiou"
	g2 = "qrtpsdfghjkzxcvbnmw"
	g3 = "csdbh"
	g = [g1 , g2 , g3]
	l = random.randint(int(lenmax/2+0.5) , lenmax)
	last = random.randint(0,1)
	targ = ""
	for i in range(l):
		if last == 0: #在元音的情况下有0.2的概率保持不变
			if random.random() < 0.2:
				last = last ^ 1
		if last == 1: #在辅音的情况下有0.2的概率再来一个辅音
			if random.random() < 0.2:
				last = 2

		last = int(last != 0) ^ 1
		targ += random.sample(g[last] , 1)[0]

	return targ

def hash(data , mod = 114514114514):
	data = pickle.dumps(data)
	data = b"yyy" + data + b"ishandsome"
	hashed = int.from_bytes(data , byteorder = "little")
	if mod > 0:
		hashed = hashed % mod
	return hashed

def strhash(data):
	data = hash(data)
	

if __name__ == "__main__":
	print (random_name())
	print (hash(None))
	print (hash(None))
	print (hash({0:[print , "oooo"] , "a" : {} , "c": {None : {233}}}))
	p = "oooo"
	d = "a"
	print (hash({0:[print ,      p] ,   d : {} , "c": {None : {233}}}))
	print (hash({d : {} , 0:[print ,      p]   , "c": {None : {233}}}))

