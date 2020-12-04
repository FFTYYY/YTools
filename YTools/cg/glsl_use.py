'''
	一个GLSL使用库
	使用ShaderProgram类来创建着色器程序
	使用Shader类来创建着色器

	沒有什麼錯誤判斷，不正確使用的話會爆炸吧大概

	TODO：最近一次测试发现不会用了
'''

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL import shaders
import types

class Shader:
	'''
		用来创建和保存一个着色器对象的类
	'''
	def __init__(self,shader_type = None , file_name = None , string = None , auto_build = True):
		'''
			从一个文件名加载，或是从一个现成的字符串。
			如果都提供了，则优先从文件名加载
			
			shader_type	：着色器类型，一个OpenGL常量
			file_name	：文件名
			string 		：字符串
			auto_build	：是否自动编译
		'''
		if file_name != None:
			self.set_data_file(file_name)
		else:
			self.set_data_string(string)

		#着色器类型
		self.shader_type = shader_type

		if auto_build:
			self.build()

	def load_from_file(self,file_name,encoding = "utf-8"):
		'''
			从文件读取一个字符串
		'''
		return open(file_name,encoding=encoding).read()

	def set_data_file(self,file_name):
		'''
			从文件加载着色器内容
		'''

		#着色器内容（源代码）
		self.data_str = self.load_from_file(file_name)

	def set_data_string(self,string):
		'''
			从字符串加载着色器内容
		'''
		self.data_str = string

	def build(self):
		'''
			创建着色器对象并编译着色器源代码
		'''

		if not self.data_str:
			raise Exception("Shader.compile() : no data")
		self.shader_object = glCreateShader(self.shader_type)
		glShaderSource(self.shader_object , self.data_str)
		glCompileShader(self.shader_object)



class ShaderProgram:
	
	def __init__(self , files = [] , strings = [] , end_create = True , use = True):
		'''
			一个着色器程序类
			可以预先指定一系列着色器内容，来添加着色器

			files		：二元组列表，每个元素为一个着色器信息，将从这些信息来自动创建着色器
							每个二元组，第一个元素为着色器类型，第二个元素为文件名
			strings		：同上，不过每个二元组的第二个元素为源代码字符串
			end_create	：是否链接这个程序
			use 		：是否激活这个程序
		'''
		self.program =  glCreateProgram()

		if files:
			for shader_type , file_name in files:
				self.add_shader_from_file(shader_type , file_name)

		if strings:
			for shader_type , string in strings:
				self.add_shader_from_string(shader_type , string)

		if end_create:
			self.end_create()

		if use:
			self.enable()

	def end_create(self):
		'''
			链接
		'''
		glLinkProgram(self.program)

	def enable(self):
		'''
			激活自己这个着色器程序
		'''
		glUseProgram(self.program)

	def disable(self):
		'''
			关闭这个程序。
			由于实际上只有一个着色器程序能处于激活状态，所以这个函数会关掉这个全局的活跃着色器，不管他是不是自己
		'''
		glUseProgram(0)

	def add_shader(self,shader):
		'''
			绑定一个着色器对象
		'''
		glAttachShader(self.program , shader.shader_object)

	def add_shader_from_string(self,shader_type,string):
		'''
			从字符串自动创建一个着色器对象，并自动绑定
		'''
		self.add_shader ( Shader(shader_type , string = string) )

	def add_shader_from_file(self,shader_type,file_name):
		'''
			从文件自动创建一个着色器对象，并自动绑定
		'''
		self.add_shader ( Shader(shader_type , file_name = file_name) )

	def update_projection_matrix(self,name):
		'''
			更新顶点着色器中的投影矩阵

			name：全局变量名
		'''
		self.set_uniform_matrix("mat_pro", glGetFloatv(GL_PROJECTION_MATRIX) , float)

	def update_modelview_matrix(self,name):
		'''
			更新建顶点着色器中的模观察矩阵

			name：全局变量名
		'''
		self.set_uniform_matrix("mat_modview", glGetFloatv(GL_MODELVIEW_MATRIX) , float)


	def set_uniform(self,uni_name,val,type_name = float):
		'''
			设置着色器中的全局变量

			uni_name	：全局变量变量名
			type_name 	：全局变量元素类型（float或者int）
			val			：一个包含了全局变量的列表，应和全局变量（如果是vec）的话的长度一致
		'''
		the_uni = glGetUniformLocation(self.program , uni_name);
		the_source = "glUniform{0}{1}(the_uni , *val)".format(len(val),type_name.__name__[0])
		exec(the_source)

	def set_uniform_matrix(self,uni_name,val,type_name = float):
		'''
			设置着色器中的全局变量

			uni_name	：全局变量变量名
			type_name 	：全局变量元素类型（float或者int）
			val			：一个包含了全局变量的列表，应和全局变量（如果是vec）的话的长度一致
		'''
		the_uni = glGetUniformLocation(self.program , uni_name)
		if len(val) == len(val[0]):
			the_source = "glUniformMatrix{0}{1}v(the_uni , 1 ,False, val)".format( len(val) , type_name.__name__[0])
		else:
			the_source = "glUniformMatrix{0}x{1}{2}v(the_uni , 1 ,False, val)".format( len(val) , len(val[0]) , type_name.__name__[0])
		exec(the_source)



