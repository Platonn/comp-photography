import numpy as np
import cv2

class AffineHelper:
	@staticmethod
	def getTranslationMatrix((y,x)):
		return np.float32([
			[1, 0, x],
			[0, 1, y]
		])

	@staticmethod
	def translate(im, (y,x)):
		M = AffineHelper.getTranslationMatrix((y,x))
		height, width, _ = im.shape
		result = cv2.warpAffine(im, M, (width, height))
		return result