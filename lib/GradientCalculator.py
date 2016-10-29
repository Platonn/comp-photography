import cv2
from scipy import ndimage

class GradientCalculator:
	FILTER_HORI = [
		[-1, 0, 1]
	]
	FILTER_VERT = [
		[-1],
		[0],
		[1]
	]

	@staticmethod
	def run(image):
		im = cv2.copyMakeBorder(image, 1, 1, 1, 1, cv2.BORDER_REFLECT_101)

		gradients_hori = ndimage.convolve(GradientCalculator.FILTER_HORI)
		gradients_vert = ndimage.convolve(GradientCalculator.FILTER_VERT)

		gradiends = gradients_hori + gradients_vert


		return gradiends[1:-1, 1:-1]