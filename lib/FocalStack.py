import numpy as np


class FocalStack:
	def __init__(self, images):
		self.images = images

	def run(self):
		imNum = len(self.images)
		imagesGradients = []
		for i in range(0, imNum):
			image = self.images[i]
			imagesGradients.append(self.__getGradientWithImageIndexChannel(image, i))

		maxArray = imagesGradients[0].copy()  # assume 1st array as maxes
		for i in range(1, imNum):  # start from 2nd array
			M = maxArray
			A = imagesGradients[i]
			# get 2 arrays: maxes array and maxes indexes array
			tempArray = np.where(M[:, :, 0] >= A[:, :, 0], [M[:, :, 0], M[:, :, 1]], [A[:, :, 0], A[:, :, 1]])
			maxArray[:, :, 0] = tempArray[0]
			maxArray[:, :, 1] = tempArray[1]
		self.maxArray = maxArray

	def getOutput(self):
		return self.maxArray[:,:,0] #return maxes without indexes

	def getContributions(self):
		imNum = len(self.images)
		contributions = []
		for i in range(imNum):
			contribution = np.where(self.maxArray[:,:,1] == i, 255, 0) # highlight if it is max
			contributions.append(contribution)
		return contributions #spike- funkcja nic nie zwraca teraz!

	def __getGradientWithImageIndexChannel(self, image, imageIndex):
		gradients = image
		(height, width) = gradients.shape
		result = np.zeros((height, width, 2), np.uint8)
		result[:, :, 0] = gradients[:, :]
		result[:, :, 1] = imageIndex
		return result