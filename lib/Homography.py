import numpy as np


class Homography:
	def __init__(self, H):
		self.H = H
		self.Hinv = np.linalg.inv(H)  # inverse matrix

	def apply(self, inputIm, outputIm):
		(height, width, channels) = inputIm.shape
		result = outputIm.copy()
		for y in range(0, height):
			for x in range(0, width):
				(newY, newX) = self.__calculate_coords(y, x)

				# fill neighbour square
				if (y < height - 2):
					yNeighbours = [0, 1]
				else:
					yNeighbours = [0]
				if (x < width - 2):
					xNeighbours = [0, 1]
				else:
					xNeighbours = [0]

				for i in yNeighbours:
					for j in xNeighbours:
						result[newY + i, newX + j] = inputIm[y, x]

		return result

	def __calculate_coords(self, y, x):
		vector = [
			[y],
			[x],
			[1]
		]
		[newY, newX, newW] = np.dot(self.Hinv, vector)
		return (int(newY / newW), int(newX / newW))