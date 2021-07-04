from django.urls import path
from django.http import HttpResponse
import pickle
import json

urlpatterns = []

def make_response_func(func , configs):
	def _resp_func(*pargs , **kwargs):
		resp = func(*pargs , **kwargs)

		if configs["encode"] == "pickle":
			resp = pickle.dumps(resp) #用pickle编码
		if configs["encode"] == "json":
			resp = json.dumps(resp) #用pickle编码
		
		resp = HttpResponse(resp)

		if configs["cross_domain"]:
			resp["Access-Control-Allow-Origin"]  = "*"
			resp["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
			resp["Access-Control-Max-Age"] 		 = "1000"
			resp["Access-Control-Allow-Headers"] = "*"

		return resp
	return _resp_func

def add_response(url , func , configs):
	urlpatterns.append(path(url , make_response_func(func , configs)))
