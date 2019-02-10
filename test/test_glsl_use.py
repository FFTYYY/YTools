'''
	兩個瑟瑟發抖的小三角形
'''

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL import shaders
from opengl_initer import *
import sys
sys.path.append("E:/Programming/Projects/Doing/Tools/")
import YYYTools.glsl_use as loader
import numpy as np
import ctypes

import time

window_w = 700
window_h = 700
window_z = 100

flash_speed = 60

progrm = None

def init_program():
	global progrm
	progrm = loader.ShaderProgram(files = [
		(GL_VERTEX_SHADER 	, "./vert.vert"),
		(GL_FRAGMENT_SHADER , "./frag.vert"),
		(GL_GEOMETRY_SHADER , "./geog.vert"),
	])

	progrm.update_projection_matrix("mat_pro")

def init_buf():
	VA_Buf = glGenBuffers(1)

	points = np.array([
		0.,0.,0.,		.8,.4,.1,
		0.,200.,0.,		.5,.4,.5,
		200.,0.,0.,		.8,.4,.8,
	] , dtype = "f")

	glBindBuffer(GL_ARRAY_BUFFER , VA_Buf)
	glBufferData(GL_ARRAY_BUFFER , points.nbytes , points , GL_STATIC_DRAW)


def draw_rec():
	glPushMatrix()

	#glColor3f(.8,.3,.3)
	glEnableVertexAttribArray(0)
	glEnableVertexAttribArray(2)

	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 4 * 6, None)
	glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 4 * 6, ctypes.c_void_p(4 * 3))
	glDrawArrays(GL_TRIANGLES, 0, 3)

	glDisableVertexAttribArray(0)
	glDisableVertexAttribArray(2)

	glPopMatrix()

def draw():
	glClear(GL_COLOR_BUFFER_BIT);
	glClear(GL_DEPTH_BUFFER_BIT);

	glMatrixMode(GL_MODELVIEW);

	progrm.set_uniform("tim",[time.clock() * 1000],float)
	progrm.set_uniform("time_for_seed",[int(time.time() * 100)],int)
	progrm.update_modelview_matrix("mat_modview")

	draw_rec();

	glFlush();

	time.sleep(1 / flash_speed);


initer = Initer(
	window_name = b"hello" , 
	window_size = (window_w,window_h) , 
	projection_args = (-window_w,window_w,-window_h,window_h,-window_z,window_z) , 
	display_func = draw , 
	idle_func = draw , 
	other_commands = [init_program , init_buf]
).init().loop()
