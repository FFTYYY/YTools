import sys
sys.path.append("E:/Programming/Projects/Doing/Tools/")
import YYYTools.debug_recursion as debug_recursion

deb = debug_recursion.RecursionDebuger()

def C(n,m):
	deb.set_point( (n,m) )
	deb.add_info("haha" , 123)

	if(m < 0 or m > n):
		deb.add_info("the_val" , 0)
		deb.end_point()
		return 0
	if(m == n):
		deb.add_info("the_val" , 1)
		deb.end_point()
		return 1

	val = C(n-1,m) + C(n-1,m-1)

	deb.add_info("the_val" , val)
	deb.end_point()

	return val


a = C(10,5)
print(a)

deb.cui.exec_()