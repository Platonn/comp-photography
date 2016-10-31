import cv2
import numpy as np


class SimpleRobertson:
	@staticmethod
	def merge(imagesWithExposures):
		meanPixelValue = 0.5
		imShape = imagesWithExposures[0][0].shape
		nominator = np.zeros(imShape, np.float32)
		denominator = nominator.copy()

		for (image, exposure) in imagesWithExposures:
			#exposure = 1/exposure #spike!!!
			print exposure
			imageExposured = image * exposure
			contributions = np.exp(-4.0 * (imageExposured - meanPixelValue) ** 2 / meanPixelValue ** 2)
			nominator += imageExposured * contributions * exposure
			denominator += contributions * exposure ** 2

		result = nominator / denominator

		return result