import numpy as np
from GradientCalculator import *

class FocalStack:
	def __init__(self, images):
		self.images = images

	def run(self):
		imNum = len(self.images)
		(height,width) = self.images[0].shape
		self.imagesGradients = np.zeros((imNum,height,width,2))
		for i in range(0, imNum):
			image = self.images[i]
			self.imagesGradients[i] = (self.__getGradientWithImageIndexChannel(image, i))

		maxArray = self.imagesGradients[0].copy()  # assume 1st array as maxes
		for i in range(1, imNum):  # start from 2nd array
			M = maxArray
			A = self.imagesGradients[i]
			# get 2 arrays: maxes array and maxes indexes array
			tempArray = np.where(M[:, :, 0] >= A[:, :, 0], [M[:, :, 0], M[:, :, 1]], [A[:, :, 0], A[:, :, 1]])
			maxArray[:, :, 0] = tempArray[0]
			maxArray[:, :, 1] = tempArray[1]
		self.maxArray = maxArray

	def getOutput(self):
		result = np.zeros(self.images[0].shape)
		imNum = len(self.images)
		contributions = self.getContributions()
		for i in range(0,imNum):

			image = self.images[i]
			contribution = contributions[i]
			print image
			print contribution

			result += image * contribution

		return (result, contributions)
		#return self.maxArray[:, :, 0]  # return maxes without indexes

	def getContributions(self):
		imNum = len(self.images)
		(height, width) = self.images[0].shape
		contributions = np.zeros((imNum,height,width))

		# SPIKE-OLD:
		# for i in range(imNum):
		# 	contribution = np.where(self.maxArray[:, :, 1] == i, 255, 0)  # highlight if it is max
		# 	contributions.append(contribution)
		for y in range(0,height):
			for x in range(0, width):
				indexOfMax = 0
				max = 0
				for i in range(0, imNum):
					gradient = self.imagesGradients[i, :, :, 0]  # get gradients only
					value = gradient[y,x]
					if(value > max):
						indexOfMax = i
						max = value

				contributions[indexOfMax][y,x] = 1


		return contributions  # spike- funkcja nic nie zwraca teraz!

	def __getGradientWithImageIndexChannel(self, image, imageIndex):
		gradients = GradientCalculator.run(image)
		(height, width) = gradients.shape
		result = np.zeros((height, width, 2), np.uint8)
		result[:, :, 0] = gradients[:, :]
		result[:, :, 1] = imageIndex
		return result