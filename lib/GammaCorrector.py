class GammaCorrector:
	def __init__(self, gamma):
		self.gamma = gamma

	def run(self, image):
		image[...] = ((image / 255.0) ** (1.0 / self.gamma)) * 255.0
