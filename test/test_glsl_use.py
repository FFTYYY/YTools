'''
	兩個瑟瑟發抖的小三角形
'''

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL import shaders

import glsl_use as loader

import time

window_width = 700;
window_height = 700;
window_z = 700;

u = 60;

progrm = None

str_ver = '''
#version 450

layout(location = 0) in vec4 position; 
//layout(location = 2) in vec4 color; 

in vec4 gl_Color;

uniform mat4 mat_pro;
uniform mat4 mat_modview;

out int my_id;
out vec4 the_color;

void main()
{
	gl_Position = mat_pro * mat_modview * position;
	my_id = gl_VertexID;
	the_color = gl_Color;
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

def draw_rec():
	glPushMatrix();

	glBegin(GL_TRIANGLES);

	glColor3f(.3,.2,.9);
	glVertex3f(0,0,0);
	glVertex3f(0,200,0);
	glVertex3f(200,0,0);

	glColor3f(.9,.4,.2);
	glVertex3f(0,0,0);
	glVertex3f(0,200,0);
	glVertex3f(200,0,0);

	glEnd();


	glPopMatrix();

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

def init():
	glClearColor(.4,.4,.4,0);
	#  glClearColor(0.,0.,0.,0);
	glViewport(0,0,window_width, window_height);

	glMatrixMode(GL_PROJECTION);
	glOrtho(-window_width/2,window_width/2,-window_height/2,window_height/2,-window_z,window_z);

	glShadeModel(GL_SMOOTH);

	glEnableClientState(GL_VERTEX_ARRAY);
	glEnableClientState(GL_TEXTURE_COORD_ARRAY);

	glEnable(GL_DEPTH_TEST);

	glEnable(GL_LINE_STIPPLE);


	glClear(GL_COLOR_BUFFER_BIT);
	glClear(GL_DEPTH_BUFFER_BIT);

	global progrm
	progrm = loader.ShaderProgram(strings = [
		(GL_VERTEX_SHADER 	, str_ver),
		(GL_FRAGMENT_SHADER , str_fra),
		(GL_GEOMETRY_SHADER , str_geo),
	])

	progrm.update_projection_matrix("mat_pro")




glutInit();

glutInitDisplayMode(GLUT_RGBA | GLUT_SINGLE | GLUT_DEPTH);
glutInitWindowSize(window_width,window_height);
glutCreateWindow(b"hello");

init();

glutDisplayFunc(draw);
glutIdleFunc(draw);


program = glCreateProgram()

glutMainLoop();
