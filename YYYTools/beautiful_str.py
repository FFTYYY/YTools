import math as M
def beautiful_str(name_list , value_list):

	vn = len(name_list)

	len_list = list(name_list)
	for i in range(vn):
		len_list[i] = len(str(name_list[i]))
		for x in value_list:
			len_list[i] = max(len_list[i] , len(str(x[i])))
		len_list[i] += 2

	def get_imm(v):
		for i in range(vn):
			v[i] = str(v[i])

		the_str = "│"

		for i in range(vn):
			the_str += (" "*M.floor((len_list[i]-len(v[i]))/2))+v[i]+(" "*M.ceil((len_list[i]-len(v[i]))/2))
			the_str += "│"

		return the_str

	ceil , imm , floor = "┌" , "├" , "└"
	for i in range(vn):
		ceil  += ("─"*len_list[i])
		imm   += ("─"*len_list[i])
		floor += ("─"*len_list[i])
		if i != vn-1:
			ceil  += "┬"
			imm   += "┼"
			floor += "┴"
		else:
			ceil  += "┐"
			imm   += "┤"
			floor += "┘"

	title = get_imm(name_list)
	cont = ""
	for x in value_list:
		cont += get_imm(x) + "\n"

	return "\n" + ceil + "\n" + title + "\n" + imm + "\n" + cont + floor

if __name__ == "__main__":
	print (beautiful_str(
		["value_1" , "v2" , "value_3"] , 
		[
			[3.14156 , 2344 , 4.5678],
			[4,5,6],
			[123,"hahahaha" , 3456,],
		]
	))
