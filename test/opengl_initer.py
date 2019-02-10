from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Initer:
	def __init__( self , 
		window_name = b"hello" , 
		window_size = (100,100) ,
		clear_color = (.4,.4,.4,0) ,
		display_mode = [GLUT_RGBA , GLUT_SINGLE , GLUT_DEPTH ,] ,
		projection_function = glOrtho ,
		projection_args = None ,
		enables = [GL_DEPTH_TEST , ] ,
		display_func = None , 
		idle_func = None ,  
		other_commands = [],
	):
		self.window_name = window_name
		self.window_size = window_size
		self.clear_color = clear_color
		self.display_mode = display_mode
		self.projection_function = projection_function

		if projection_args is None:
			if projection_function is glOrtho:
				self.projection_args = [
					-window_size[0] , 
					 window_size[0] , 
					-window_size[1] , 
					 window_size[1] , 
					 -100, 100 ,
				]
			else : pass #TODO
		else : self.projection_args = projection_args

		self.enables = enables
		self.display_func = display_func
		self.idle_func = idle_func
		self.other_commands = other_commands

	def unnes_init(self):
		w , h = self.window_size
		glClearColor(*self.clear_color)
		glViewport(0,0,w,h)

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		self.projection_function(*self.projection_args)

		for x in self.enables:
			glEnable(x)

		for x in self.other_commands:
			if callable(x):
				x()
			else:
				exec(x)

	def init(self):
		glutInit();

		display_mode = 0
		for x in self.display_mode:
			display_mode |= x
		glutInitDisplayMode(x)

		glutInitWindowSize(self.window_size[0] , self.window_size[1])
		glutCreateWindow(self.window_name)

		self.unnes_init()

		if self.display_func:
			glutDisplayFunc(self.display_func)
		if self.idle_func:
			glutIdleFunc(self.idle_func)
		return self
	
	def loop(self):
		glutMainLoop()
		return self
		
