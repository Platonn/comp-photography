import numpy as np
import cv2
import sys
from LabFiles import *
from lib.utils.Normalizer import *
from lib.utils.Timer import *


def prepareMatrixL(p1, p2, p3):
	y, x, z = 0, 1, 2
	return np.array([
		[p1[x], p1[y], p1[z]],
		[p2[x], p2[y], p2[z]],
		[p3[x], p3[y], p3[z]]
	])


def calculateNormals(im1, im2, im3, p1, p2, p3):
	Timer.start('calculateNormals')
	L = prepareMatrixL(p1, p2, p3)
	print L
	Linv = np.linalg.inv(L)
	print Linv
	# raise None
	(h, w) = im1.shape
	result = np.zeros((h, w, 3), dtype=np.float32)
	for y in range(0, h):
		for x in range(0, w):
			I = np.array([im1[y, x], im2[y, x], im3[y, x]])
			N = np.dot(Linv, I)
			lengthN = np.linalg.norm(N)
			if lengthN == 0:
				normalizedN = np.array([0, 0, 0])
			else:
				normalizedN = N / lengthN
			result[y, x] = normalizedN
	print result
	Timer.stop('calculateNormals')
	return result


def zerosToEpsilon(channel):
	epsilon = sys.float_info.epsilon
	channelWithoutZeors = np.where(channel == 0, epsilon, channel)
	return channelWithoutZeors


def colorizeNormals(normals):
	y, x, z = 0, 1, 2
	b, g, r = 0, 1, 2
	zChannel = normals[:, :, z]
	zChannelWithoutZeors = zerosToEpsilon(zChannel)
	normals[:, :, z] = zChannelWithoutZeors
	normals[:, :, y] /= normals[:, :, z]
	normals[:, :, x] /= normals[:, :, z]

	result = np.zeros(normals.shape)
	result[:, :, g] = normals[:, :, x]
	result[:, :, r] = normals[:, :, y]
	result = Normalizer.to8bit((result))
	return result


### MAIN:
Timer.start('program')

im1 = cv2.imread(LabFiles.input(5, 1, 'teapot_0_-1_1'), cv2.IMREAD_GRAYSCALE)
im2 = cv2.imread(LabFiles.input(5, 1, 'teapot_1_1_1'), cv2.IMREAD_GRAYSCALE)
im3 = cv2.imread(LabFiles.input(5, 1, 'teapot_-1_1_1'), cv2.IMREAD_GRAYSCALE)
p1 = np.array([-1, 0, 1])
p2 = np.array([1, 1, 1])
p3 = np.array([1, -1, 1])

normals = calculateNormals(im1, im2, im3, p1, p2, p3)
print normals

result = colorizeNormals(normals)

cv2.imwrite(LabFiles.output(5, 1, 'teapot-normals-red-green-unitZ'), result)

# stoper
Timer.stop('program')

# show
LabFiles.show(5, 1, 'teapot-normals-red-green-unitZ')