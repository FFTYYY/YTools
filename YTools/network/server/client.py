import urllib.request
import pickle

def request(url , ip = "127.0.0.1" , port = "8000"):
	full_url = "http://{ip}:{port}/{url}".format(ip = ip , port = port , url = url)
	response = urllib.request.urlopen(full_url).read()
	return pickle.loads(response)

class Requester:
	def __init__(self , ip = "127.0.0.1" , port = "30726"):
		self.ip = ip
		self.port = port
	def request(self , url):
		return request(url , self.ip , self.port)