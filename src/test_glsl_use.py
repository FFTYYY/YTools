'''
	兩個瑟瑟發抖的小三角形
'''

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL import shaders
from opengl_easy_use import *

import glsl_use as loader
import numpy as np
import ctypes

import time

window_w = 700
window_h = 700
window_z = 100

u = 60;

progrm = None

str_ver = '''
#version 450

layout(location = 0) in vec4 position; 
//layout(location = 2) in vec4 color; 
layout(location = 2) in vec3 my_color; 

//in vec4 gl_Color;

uniform mat4 mat_pro;
uniform mat4 mat_modview;

out int my_id;
out vec4 the_color;

void main()
{
	gl_Position = mat_pro * mat_modview * position;
	my_id = gl_VertexID;
	the_color = vec4(my_color.rgb , 0);
}
'''

str_fra = '''
#version 450

in vec4 my_color;

void main()
{
	gl_FragColor = my_color;
}
'''

str_geo = '''
#version 450

layout (triangles) in;
layout (triangle_strip, max_vertices = 3) out;

in vec4 the_color[];
out vec4 my_color;

in int my_id[];

uniform vec2 fix;
uniform float tim;
uniform int now_time;

uint next = 1;
uint myrand(void) 
{
    next = (next * 1103515245 + 12345);
    return uint((next / 65536u) % 32768u);
}

float rand()
{
    return (float(myrand()) / 32768. - 0.5) / 20.;
}

void mysrand(uint seed) 
{
    next = seed;
}

void main() 
{
    mysrand(uint(now_time));

    for(int i = 0;i < 3;i++)
    {
        float val = tim * 30;
        float the_f = float(my_id[i]) / 2.;
        val *= the_f;

        if(my_id[i] < 3)
            val = -val;

        vec4 rd = vec4(rand() , rand() , rand() , 0);

        gl_Position = gl_in[i].gl_Position + vec4(val,0.0,0.0,0) + rd;
        my_color = the_color[i];
        EmitVertex();
    }

    EndPrimitive();
}

'''


def init_program():
	global progrm
	progrm = loader.ShaderProgram(strings = [
		(GL_VERTEX_SHADER 	, str_ver),
		(GL_FRAGMENT_SHADER , str_fra),
		(GL_GEOMETRY_SHADER , str_geo),
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

	progrm.set_uniform("tim",[time.clock() / 1000],float)
	progrm.set_uniform("fix",[-0.5,0],float)
	progrm.set_uniform("now_time",[int(time.time() * 100)],int)
	progrm.update_modelview_matrix("mat_modview")

	draw_rec();

	glFlush();

	time.sleep(1 / 60);


initer = Initer(
	window_name = b"hello" , 
	window_size = (window_w,window_h) , 
	projection_args = (-window_w,window_w,-window_h,window_h,-window_z,window_z) , 
	display_func = draw , 
	idle_func = draw , 
	other_commands = [init_program , init_buf]
).init().loop()
