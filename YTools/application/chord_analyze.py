from YTools.universe.beautiful_str import beautiful_str

def 音高差(x,y , k = -1):
	'''x和y的音高差是否为k
	如果k为None，则返回x和y的音高差，顺序是任意的（比如，差7等价于差5）
	'''
	diff = (((x - y) % 12) + 12) % 12
	if k < 0:
		return diff
	return diff == k or (12 - diff) == k


def 规范(x):
	return ((x % 12) + 12) % 12

def 规范等同(x,y):
	return 规范(x) == 规范(y)

def has(s):
	for x in s:
		if x:
			return True
	return False

class 调式:
	def __init__(self , 名 , 音阶差分):

		self.名 = 名
		if len(音阶差分) != 7:
			raise ValueError("不支持不是7个音的音阶")
		if sum(音阶差分) != 12:
			raise ValueError("必须是12个半音")

		self.音阶差分 = 音阶差分[:-1] #去掉最后一个

	def 音(self , k):
		'''第k个音比主音高多少'''
		flag = 0 #是否升半音
		if k - int(k) != 0:
			flag = 1
			k = int(k)

		k = (k-1 + 7) % 7
		s = 0
		for x in range(k):
			s += self.音阶差分[x]
		return 规范(s + flag)

	def 生成和弦(self , 组成音, 低音 = None):
		return {
			"组成": [self.音(x) for x in 组成音] , 
			"低音": self.音(组成音[0]) if 低音 is None else self.音(低音) , 
		}	

	def 构造和弦(self, 类型, 根音):

		根音 = self.音(根音)
		组成 = []
		if 类型 == "属":
			组成 = [根音, 根音+4, 根音+7, 根音+10]
		if 类型 == "大":
			组成 = [根音, 根音+4, 根音+7]
		if 类型 == "小":
			组成 = [根音, 根音+3, 根音+7]
		if 类型 == "减":
			组成 = [根音, 根音+3, 根音+6]

		return {
			"组成": [规范(x) for x in 组成], 
			"低音": 规范(根音) , 
		}


	def 存在属进行(self , 和弦):
		'''是否和主和弦成属进行'''
		return 规范等同(和弦["低音"] , 7) #比主音高五度


	def 存在下属进行(self , 和弦):
		'''是否和主和弦成下属进行'''
		return 规范等同(和弦["低音"] , 5) #比主音低五度

	def 存在三全音(self , 和弦):
		return has( [音高差(x,y,6) for x in 和弦["组成"] for y in 和弦["组成"]] )

	def 存在半音关系(self , 和弦 , 主和弦类型 = "三"):
		主和弦 = []
		if 主和弦类型 == "三":
			主和弦 = [1,3,5]
		elif 主和弦类型 == "七": 
			主和弦 = [1,3,5,7]
		else:
			raise ValueError("不支持！")

		主和弦 = self.生成和弦(主和弦)

		cnt = 0
		for x in 和弦["组成"]:
			for y in 主和弦["组成"]: #在主和弦的组成音中有和x成半音的
				if 音高差(x,y,1) : 
					cnt += 1
					break

		return cnt
	def 存在导音(self , 和弦):
		return has( [规范等同(x , 11) for x in 和弦["组成"]] )

	def 报告属性(self , 和弦集合):

		report = []

		for 名 , 和弦组成音 , 低音 in 和弦集合:

			if isinstance(和弦组成音 , str):
				和弦 = self.构造和弦(和弦组成音 , 低音)
			else:
				和弦 = self.生成和弦(和弦组成音 , 低音)


			五度进行  = ""
			if self.存在属进行(和弦):
				五度进行 = "属"
			elif self.存在下属进行(和弦):
				五度进行 = "下属"

			三全音    = "V" if self.存在三全音(和弦) else ""
			半音关系_三  = self.存在半音关系(和弦 , 主和弦类型 = "三")
			半音关系_七  = self.存在半音关系(和弦 , 主和弦类型 = "七")
			导音      = "V" if self.存在导音(和弦) else ""

			report.append( [str(名) , str(五度进行) , str(三全音) , str(导音) , str(半音关系_三) , str(半音关系_七)] )

		with open("a.txt" , "a+") as fil:
			fil.write(self.名 + "\n")
			for x in report:
				for y in x:
					fil.write(str(y) + ",")
				fil.write("\n")

		report = beautiful_str(["名" , "五度进行" , "三全音" , "导音" , "半音关系（主3）" , "半音关系（主7）"] , report)
		return self.名 + report

if __name__ == "__main__":

	和弦集合 = [
		["属三"       	, [5,7,2]   		, None 	] , 
		["属七"       	, [5,7,2,4] 		, None 	] , 
		["七级三"     	, [7,2,4]   		, None 	] , 
		["三全音代理" 	, "属" 				, 4.5 	] , 

		["下属三"     	, [4,6,1]         	, None 	] , 
		["下属七"     	, [4,6,1,3]       	, None 	] , 
		["属系分数"    	, [5,4,6,1]   		, 5 	] , 
		["下属小" 		, "小" 				, 4 	] , 
	]

	

	print (调式("大调式"     , [2,2,1,2,2,2,1]).报告属性(和弦集合) + "\n")
	print (调式("小调式"     , [2,1,2,2,1,2,2]).报告属性(和弦集合) + "\n")
	print (调式("和声小调式" , [2,1,2,2,1,3,1]).报告属性(和弦集合) + "\n")
	print (调式("旋律小调式" , [2,1,2,2,2,2,1]).报告属性(和弦集合) + "\n")