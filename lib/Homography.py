import numpy as np
import math


class Homography:
	def __init__(self, H):
		self.H = H

	# self.Hinv = np.linalg.inv(H)  # inverse matrix

	def applyNeighbour(self, inputIm, outputIm):
		result = outputIm.copy()
		(height, width, _) = outputIm.shape
		for y in range(0, height):
			for x in range(0, width):
				(yIn, xIn) = self.__calculate_coords(y, x)
				if self.__isInImage(yIn, xIn, inputIm):
					result[y, x] = self.__getNearestNeighbourValue(yIn, xIn, inputIm)
		return result

	def applyInterpolated(self, inputIm, outputIm):
		result = outputIm.copy()
		(height, width, _) = outputIm.shape
		for y in range(0, height):
			for x in range(0, width):
				(yIn, xIn) = self.__calculate_coords(y, x)
				if self.__isInImage(yIn, xIn, inputIm):
					result[y, x] = self.__getInterpolatedValue(yIn, xIn, inputIm)
		return result

	def __isInImage(self, Y, X, im):
		(inHeight, inWidth, _) = im.shape
		return Y >= 0 and \
		       Y <= inHeight - 1 and \
		       X >= 0 and \
		       X <= inWidth - 1

	def __getNearestNeighbourValue(self, Y, X, im):
		(yNew, xNew) = (int(round(Y)), int(round(X)))
		return im[yNew, xNew]

	def __getInterpolatedValue(self, y, x, im):
		# A B
		# C D
		# distances to grid points:
		topDist = math.modf(y)[0]
		bottomDist = 1. - topDist
		leftDist = math.modf(x)[0]
		rightDist = 1. - leftDist

		top = int(y)
		bottom = top + 1
		left = int(x)
		right = left + 1

		A = self.__getPixelReflect101(top, left, im)
		B = self.__getPixelReflect101(top, right, im)
		C = self.__getPixelReflect101(bottom, left, im)
		D = self.__getPixelReflect101(bottom, right, im)

		#print A, B, C, D

		aDist = self.__pitagoras(topDist, leftDist)
		bDist = self.__pitagoras(topDist, rightDist)
		cDist = self.__pitagoras(bottomDist, leftDist)
		dDist = self.__pitagoras(bottomDist, rightDist)

		sumDist = aDist + bDist + cDist + dDist

		aWeight = sumDist - aDist
		bWeight = sumDist - bDist
		cWeight = sumDist - cDist
		dWeight = sumDist - dDist

		sumWeight = aWeight + bWeight + cWeight + dWeight

		aContrib = aWeight / sumWeight
		bContrib = bWeight / sumWeight
		cContrib = cWeight / sumWeight
		dContrib = dWeight / sumWeight

		result = A * aContrib + \
		         B * bContrib + \
		         C * cContrib + \
		         D * dContrib

		return result

	def __pitagoras(self, y, x):
		return math.sqrt(y * y + x * x)

	def __getPixelReflect101(self, y, x, im):
		(height, width, _) = im.shape
		if y < 0: y = -y
		if y > height - 1: y = 2 * height - y -1
		if x < 0: x = -x
		if x > width - 1: x = 2 * width - x -1
		return im[y,x]


	def __bilinearInterpolate(self, Y, X):
		yFract = math.modf(Y)
		xFract = math.modf(X)

	def __calculate_coords(self, y, x):
		vector = [
			[y],
			[x],
			[1]
		]
		[newY, newX, newW] = np.dot(self.H, vector)
		return ((newY / newW), (newX / newW))
