import os
import os.path as P
import pickle
from .filename import hash

def try_load(key, path = ".", force_reload = False):
	if force_reload:
		return None
	filename = P.join(path , str(hash(key)))

	if P.exists(filename):
		with open(filename , "rb") as fil:
			data = pickle.load(fil)
		return data
	return None

def save_data(key , data , path = "."):
	filename = P.join(path , str(hash(key)))
	with open(filename , "wb") as fil:
		pickle.dump(data , fil)
