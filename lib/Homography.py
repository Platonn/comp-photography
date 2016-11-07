import numpy as np


class Homography:
	def __init__(self, H):
		self.H = H
		self.Hinv = np.linalg.inv(H)  # inverse matrix

	# TODO: interpolate missing values - image has stretch marks
	def apply(self, inputIm, outputIm):
		(height, width, channels) = inputIm.shape
		result = outputIm.copy()
		for y in range(0, height):
			for x in range(0, width):
				(newY, newX) = self.__calculate_coords(y, x)
				result[newY, newX] = inputIm[y, x]
		return result

	def __calculate_coords(self, y, x):
		vector = [
			[y],
			[x],
			[1]
		]
		[newY, newX, newW] = np.dot(self.Hinv, vector)
		return (int(newY / newW), int(newX / newW))