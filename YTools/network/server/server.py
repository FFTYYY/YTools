import os
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.urls import path
from pathlib import Path
from .urlconf import add_response

def start_server(ip = "0.0.0.0", port = "30726", responsers = {} , encode = "pickle" , cross_domain = False):

	configs = {
		"encode" : encode , 
		"cross_domain": cross_domain , 
	}

	for url , func in responsers.items():
		add_response(url , func , configs)

	settings.configure(
		DEBUG = True,	
		ROOT_URLCONF = "YTools.network.server.urlconf", 
		SECRET_KEY = "THEWORLD", # unsafe!!
	)
	django.setup()

	ipaddr = "{ip}:{port}".format(ip = ip , port = port)
	execute_from_command_line(["" , "runserver" , ipaddr])