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