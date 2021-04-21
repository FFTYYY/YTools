import os
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.urls import path
from pathlib import Path
from .urlconf import add_response

def start_server(ip = "0.0.0.0", port = "30726", responsers = {}):

	for url , func in responsers.items():
		add_response(url , func)

	settings.configure(
		DEBUG = True,	
		ROOT_URLCONF = "YTools.network.server.urlconf", 
	)
	django.setup()

	ipaddr = "{ip}:{port}".format(ip = ip , port = port)
	execute_from_command_line(["" , "runserver" , ipaddr])