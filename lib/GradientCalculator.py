import cv2
from scipy import ndimage
import numpy as np

class GradientCalculator:
	FILTER_HORI = [
		[-1.0, 0, 1.0]
	]
	FILTER_VERT = [
		[-1.0],
		[0.0],
		[1.0]
	]

	@staticmethod
	def run(image):
		im = cv2.copyMakeBorder(image.astype('float32'), 1, 1, 1, 1, cv2.BORDER_REFLECT_101)

		gradients_hori = ndimage.convolve(im, GradientCalculator.FILTER_HORI)
		gradients_vert = ndimage.convolve(im, GradientCalculator.FILTER_VERT)

		gradiends = np.absolute(gradients_hori) + np.absolute(gradients_vert)


		return gradiends[1:-1, 1:-1]