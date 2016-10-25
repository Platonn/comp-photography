import cv2
import numpy as np
from GammaCorrector import *


class ChrominanceMedianFilterer:
	def __init__(self, rawImage):
		self.tempImage = rawImage

	def run(self):
		imageYCrCb = cv2.cvtColor(self.tempImage, cv2.COLOR_BGR2YCR_CB)
		imageYCrCb = self.__chrominanceMedianFilter(imageYCrCb, 10)
		self.tempImage = cv2.cvtColor(imageYCrCb, cv2.COLOR_YCR_CB2BGR)

	def saveOutput(self, fileName):
		cv2.imwrite(fileName, self.tempImage)

	def __chrominanceMedianFilter(self, imageYCrCb, radius):
		im = cv2.copyMakeBorder(imageYCrCb, radius, radius, radius, radius, cv2.BORDER_REFLECT_101)
		imOut = im.copy()
		Cb = 1
		Cr = 2
		r = radius
		(height, width, channels) = im.shape
		for y in range(r, height - r):
			for x in range(r, width - r):
				# print y, x
				imOut[y, x, Cb] = np.mean(im[(y - r):(y + r), (x - r):(x + r), Cb])
				imOut[y, x, Cr] = np.mean(im[(y - r):(y + r), (x - r):(x + r), Cr])

		imResult = imOut[r:-r, r:-r]
		return imResult

	def correctGamma(self):
		GammaCorrector(2.2).run(self.tempImage)