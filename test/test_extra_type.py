import sys
sys.path.append("../YYYTools/")
from extra_type import *

def func(g , o = 12):
	print ("g = ",g,"o = ",o)

s = Struct(123 , 4 , 5 , g = 233 , o = 7)
