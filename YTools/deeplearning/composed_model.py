import torch as tc

class EnsembleModel:
	'''Ensemble模型

	只可用于测试，不要训练这个模型。
	另外注意这个类会自动取softmax，所以要保证模型中没有取softmax，loss函数中也不会取softmax

	参数：
	models：要混合的模型
	device：在哪个设备上混合。
		其实对小模型无所谓的，有这个选项主要是允许把model都放到cpu上，每次只取一个model在gpu上生成，以节省
		显存。
	'''

	def __init__(self , models , device = 0):
		self.models = models
		self.device = device

	def forward(self , *pargs , output_preds = False , **kwargs):
		models = self.models
		device = self.device

		with tc.no_grad():
			preds = [0 for _ in range(len(models))]
			for i , model in enumerate(models):

				old_device = next(model.parameters()).device
				model = model.to(device)
				preds[i] = model(*pargs , **kwargs)
				model = model.to(old_device) #如果他本来在cpu上，生成完之后还是把他放回cpu

		if output_preds:
			return preds

		pred = 0
		for x in preds:
			pred = pred + tc.softmax(x , dim = -1)
		pred /= len(models)

		return pred

	def __call__(self , *pargs , **kwargs):
		return self.forward(*pargs , **kwargs)

	@property
	def parameters(self): #for device deciding
		return self.models[0].parameters

	def to(self , device):
		self.device = device
		return self

	def eval(self):
		for i in range(len(self.models)):
			self.models[i] = self.models[i].eval()
		return self
	def train(self):
		for i in range(len(self.models)):
			self.models[i] = self.models[i].train()
		return self

