import cv2
from GammaCorrector import *


class Demosaicer:
	def __init__(self, rawImage):
		self.rawImage = rawImage
		self.tempImage = cv2.copyMakeBorder(self.rawImage, 1, 1, 1, 1, cv2.BORDER_REFLECT_101)
		self.outImage = rawImage.copy()

	def saveOrigin(self, fileName):
		cv2.imwrite(fileName, self.rawImage)

	def saveOutput(self, fileName):
		self.__temp2output()
		cv2.imwrite(fileName, self.outImage)

	def __temp2output(self):
		self.outImage[:, :] = self.tempImage[1:-1, 1:-1]

	def correctGamma(self, gamma=2.2):
		GammaCorrector(gamma).run(self.tempImage)