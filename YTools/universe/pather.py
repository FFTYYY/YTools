import os.path as P

def relative_path(this_file , rel_path):
	return P.join(P.dirname(this_file) , rel_path)