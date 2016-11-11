import numpy as np
import math

class Homography:
	def __init__(self, H):
		self.H = H

	def applyNeighbour(self, inputIm, outputIm):
		result = outputIm.copy()
		(height, width, _) = outputIm.shape
		for y in range(0, height):
			for x in range(0, width):
				(yIn, xIn) = self.__calculateCoords(y, x)
				if not self.__isOutOfImage(yIn, xIn, inputIm):
					(yNew, xNew) = self.__getNearestNeighbourCoords(yIn, xIn)
					result[y, x] = inputIm[yNew, xNew]
		return result

	def applyInterpolated(self, inputIm, outputIm, newShape=(0,0), offset=(0, 0)):
		outHeight, outWidth, _ = outputIm.shape
		(yOffset, xOffset) = offset

		# copy outputIm to result
		if newShape == (0,0):
			result = outputIm.copy()
		else:
			shape = newShape[0], newShape[1], outputIm.shape[2]
			result = np.zeros(shape, outputIm.dtype)
			result[yOffset:(yOffset + outHeight), xOffset:(xOffset + outWidth)] = outputIm

		# warp inputIm into result
		height, width, _ = result.shape
		for y in range(0, height):
			for x in range(0, width):
				(y_pos, x_pos) = self.__calculateCoords(y - yOffset, x - xOffset, self.H)
				interpolatedValue = self.__getInterpolatedValue(y_pos, x_pos, inputIm)
				if interpolatedValue != None:
					result[y, x] = interpolatedValue
		return result

	def calculateCornersCoords(self, image):
		(height, width, _) = image.shape

		corners = np.array([(0, 0), (0, width - 1), (height - 1, 0), (height - 1, width - 1)])
		print corners
		Hinv = np.linalg.inv(self.H)

		newCornersX, newCornersY = np.zeros(4), np.zeros(4)
		for i in range(0, 4):
			(y, x) = corners[i]
			newY, newX = self.__calculateCoords(y, x, Hinv)
			newY, newX = self.__getNearestNeighbourCoords(newY, newX)
			newCornersY[i] = newY
			newCornersX[i] = newX

		return (newCornersY, newCornersX)

	def getNewShapeAndOffset(self, inputIm, outputIm):
		invH = np.linalg.inv(self.H)
		outHeight, outWidth, outChannels = outputIm.shape
		inHeight, inWidth, _ = inputIm.shape
		inCorners = [(0, 0), (0, inWidth - 1), (inHeight - 1, 0), (inHeight - 1, inWidth - 1)]

		inCornersNewY = []
		inCornersNewX = []
		for (yIn, xIn) in inCorners:
			(inNewY, inNewX) = self.__calculateCoords(yIn, xIn, invH)
			inCornersNewY.append(int(inNewY))
			inCornersNewX.append(int(inNewX))

		outCornersY = [0, outHeight]
		outCornersX = [0, outWidth]

		allCornersY = outCornersY + inCornersNewY
		allCornersX = outCornersX + inCornersNewX

		minY, minX = min(allCornersY), min(allCornersX)
		maxY, maxX = max(allCornersY), max(allCornersX)

		resultNewShape = (maxY - minY, maxX - minX, outChannels)
		resultOffset = (0 - minY, 0 - minX)

		return resultNewShape, resultOffset

	def __isOutOfImage(self, Y, X, im):
		(inHeight, inWidth, _) = im.shape
		return Y < 0 or Y > inHeight - 1 or X < 0 or X > inWidth - 1

	def __getNearestNeighbourCoords(self, Y, X):
		return (int(round(Y)), int(round(X)))

	def __getInterpolatedValue(self, y, x, im):
		height, width, _ = im.shape
		y1, y2 = int(y), int(y) + 1
		x1, x2 = int(x), int(x) + 1
		corners = np.array([[y1, x1], [y1, x2], [y2, x1], [y2, x2]])
		if (corners > 0).all() and \
				(corners[:, 0] < height).all() and \
				(corners[:, 1] < width).all():  # check if in bounds
			p11 = im[y1, x1]
			p12 = im[y1, x2]
			p21 = im[y2, x1]
			p22 = im[y2, x2]
			resP11 = p11 * ((y2 - y) * (x2 - x))
			resP12 = p12 * ((y2 - y) * (x - x1))
			resP21 = p21 * ((y - y1) * (x2 - x))
			resP22 = p22 * ((y - y1) * (x - x1))
			result = resP11 + resP12 + resP21 + resP22
		else:
			result = None
		return result

	def __calculateCoords(self, y, x, H=[]):
		if H == []:  # default argument
			H = self.H
		vector = [
			[y],
			[x],
			[1]
		]
		[newY, newX, newW] = np.dot(H, vector)
		return ((newY / newW), (newX / newW))
