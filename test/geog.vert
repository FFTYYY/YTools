#version 450

layout (triangles) in;
layout (triangle_strip, max_vertices = 300) out;

in vec4 the_color[];
out vec4 my_color;

in int my_id[];

uniform float tim;
uniform int time_for_seed;

vec4 get_fix(float pos,int i)
{
	if(i != 0)
		return vec4(0,0,0,0);
	return vec4(tim / 20000 , 0 , 0 , 0);
}

float get_r_fix()
{
	int gap = 50;
	int lif = 70;
	int tim_val = int(tim / float(gap)) % lif;
	float x = float(tim_val) / float(lif);
	float res = sin(x * 3.14159);

	//res = (cos(x * 2 * 3.14159) + 1.) / 2.;

	return res;
}

float get_theta_fix()
{	
	int gap = 10;
	int lif = 720;
	int tim_val = int(tim / float(gap)) % lif;
	float x = float(tim_val) / float(lif);
	float res = x;

	return res;
}

float get_theta_fix_2()
{	
	int gap = 21;
	int lif = 40;
	int tim_val = int(tim / float(gap)) % lif;
	float x = float(tim_val) / float(lif);
	float res = x;

	return res;
}

void main() 
{
	vec4 point = (gl_in[0].gl_Position + gl_in[1].gl_Position + gl_in[2].gl_Position) / 3;
	vec4 new_pos[3];
	for(int i = 0;i < 3;i++)
	{
		new_pos[i] = (gl_in[i].gl_Position - point) / 5. + point;
	}

	float pi = 3.14159;
	float r = .8 * get_r_fix();
	int n = 42;
	for(int k = 0;k < n;k++)
	{
		float pos = float(k) / float(n);
		float ang = (pos - get_theta_fix()) * 2 * pi;
		for(int i = 0;i < 3;i++)
		{
			vec4 my_pos = new_pos[i];

			{
				my_pos -= point;
				float the = (pos - get_theta_fix()) * 2 * pi;
				my_pos = vec4(
					my_pos.x * cos(the) + my_pos.y * sin(the) , 
					-my_pos.x * cos(the) + my_pos.y * sin(the) , 
					my_pos.zw
				);
				my_pos += point;
			}

			my_pos.x += r * cos(ang);
			my_pos.y += r * sin(ang);
			gl_Position = my_pos;
			my_color = the_color[i];
			EmitVertex();
		}
		EndPrimitive();
	}

}   