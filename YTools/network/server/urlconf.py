from django.urls import path
from django.http import HttpResponse
import pickle

urlpatterns = []

def make_response_func(func):
	def _resp_func(*pargs , **kwargs):
		resp = func(*pargs , **kwargs)
		resp = pickle.dumps(resp)
		return HttpResponse(resp)
	return _resp_func

def add_response(url , func):
	urlpatterns.append(path(url , make_response_func(func)))
