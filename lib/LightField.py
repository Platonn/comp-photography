import cv2
import numpy as np
import itertools
from LabFiles import *
from lib.utils.Timer import *
from lib.utils.Normalizer import *

from lib.utils.AffineHelper import *


class LightField:
	@staticmethod
	def readLightField(name, number):
		Timer.start('readLightField')
		im = cv2.imread(LabFiles.input(7, 1, name))
		totalHeight, totalWidth, channels = im.shape
		height, width = totalHeight / number, totalWidth / number
		result = np.zeros((number, number, height, width, channels))
		for i in range(0, number):
			for j in range(0, number):
				croppedIm = im[(i * height):((i + 1) * height), (j * width):((j + 1) * width)]
				result[i, j] = croppedIm
			# cv2.imwrite(LabFiles.output(7, 1, 'matrioska-' + str(i) + '-' + str(j)), croppedIm) #spike
		Timer.stop('readLightField')
		return result

	@staticmethod
	def getApertureView(images, borderWidth):
		Timer.start('getApertureView')
		numVertical, numHorizontal, height, width, channels = images.shape
		result = np.zeros(((numVertical + borderWidth) * height, (numHorizontal + borderWidth) * width, channels))
		for i in range(0, numVertical):
			for j in range(0, numHorizontal):
				result[i::numVertical + borderWidth, j::numHorizontal + borderWidth] = images[i, j]
		Timer.stop('getApertureView')
		return result

	@staticmethod
	def getHorizontalCenterLine(images, i, j):
		numVertical, numHorizontal, height, width, channels = images.shape
		centerHorizontalLineId = height / 2
		result = images[i, j, centerHorizontalLineId, :]
		return result

	@staticmethod
	def getVerticalCenterLine(images, i, j):
		numVertical, numHorizontal, height, width, channels = images.shape
		centerVerticalLineId = width / 2
		result = images[i, j, :, centerVerticalLineId]
		return result

	# getHorizontalSlice:
	@staticmethod
	def getHorizontalSliceByRow(images, rowId):
		numVertical, numHorizontal, height, width, channels = images.shape
		result = np.zeros((numHorizontal, width, 3))
		for colId in range(0, numHorizontal):
			result[colId] = LightField.getHorizontalCenterLine(images, rowId, colId)
		return result

	# spike - nie ma sensu
	# @staticmethod
	# def getHorizontalSliceByCol(images, colId):
	# 	numVertical, numHorizontal, height, width, channels = images.shape
	# 	result = np.zeros((numHorizontal, width, 3))
	# 	for rowId in range(0, numHorizontal):
	# 		result[rowId] = LightField.getHorizontalCenterLine(images, rowId, colId)
	# 	return result

	# getVerticalSlice:
	@staticmethod
	def getVerticalSliceByCol(images, colId):
		numVertical, numHorizontal, height, width, channels = images.shape
		result = np.zeros((height, numVertical, 3))
		for rowId in range(0, numHorizontal):
			result[:, rowId] = LightField.getVerticalCenterLine(images, rowId, colId)
		return result

	# spike - nie ma sensu
	# @staticmethod
	# def getVerticalSliceByRow(images, rowId):
	# 	numVertical, numHorizontal, height, width, channels = images.shape
	# 	result = np.zeros((height, numVertical, 3))
	# 	for colId in range(0, numHorizontal):
	# 		result[colId] = LightField.getVerticalCenterLine(images, rowId, colId)
	# 	return result

	# get slices:
	@staticmethod
	def getHorizontalSlices(images):
		Timer.start('getHorizontalSlices')
		numVertical, numHorizontal, height, width, channels = images.shape
		result = np.zeros(((numVertical) * numHorizontal, width, channels))
		for i in range(0, numVertical):
			sliceIm = LightField.getHorizontalSliceByRow(images, i)
			result[(numHorizontal * i):(numHorizontal * (i + 1)), :] = sliceIm
		# cv2.imwrite(LabFiles.output(7,2, name + '-sliceHorizontal-row' + str(rowId)), sliceIm)
		Timer.stop('getHorizontalSlices')
		return result

	@staticmethod
	def getVerticalSlices(images):
		Timer.start('getVerticalSlices')
		numVertical, numHorizontal, height, width, channels = images.shape
		result = np.zeros((height, (numHorizontal) * numVertical, channels))
		for j in range(0, numVertical):
			sliceIm = LightField.getVerticalSliceByCol(images, j)
			result[:, (numVertical * j):(numVertical * (j + 1))] = sliceIm
		# cv2.imwrite(LabFiles.output(7,2, name + '-sliceHorizontal-row' + str(rowId)), sliceIm)
		Timer.stop('getVerticalSlices')
		return result

	@staticmethod
	def normalizeImages(images):
		numVertical, numHorizontal, height, width, channels = images.shape
		for i in range(0, numVertical):
			for j in range(0, numHorizontal):
				images[i, j] = Normalizer.normalize(images[i, j])
		return images

	@staticmethod
	def to8BitImages(images):
		numVertical, numHorizontal, height, width, channels = images.shape
		for i in range(0, numVertical):
			for j in range(0, numHorizontal):
				images[i, j] = Normalizer.to8bit(images[i, j])
		return images

	@staticmethod
	def merge(images, radius):
		numVertical, numHorizontal, height, width, channels = images.shape
		result = np.zeros((height, width, channels))
		centerVertical = numVertical/2
		centerHorizontal = numHorizontal / 2
		for i in range(centerVertical-radius, centerVertical+radius+1):
			for j in range(centerHorizontal-radius, centerHorizontal+radius+1):
				result += images[i, j]

		weight = 1.0 / float(1.0 + 2*radius)**2
		result = result * weight
		return result

	@staticmethod
	def displace(images, displacement):
		numVertical, numHorizontal, height, width, channels = images.shape
		result = np.zeros(images.shape)
		centerVertical = numVertical/2
		centerHorizontal = numHorizontal / 2

		for i in range(0,numVertical):
			for j in range(0, numHorizontal):
				localDisplacementVertical = displacement * (i - centerVertical)
				localDisplacementHorizontal = displacement * (j - centerHorizontal)
				im = images[i,j]
				result[i,j] = AffineHelper.translate(im, (localDisplacementVertical, localDisplacementHorizontal))

		return result


	@staticmethod
	def displacementVideo(fileName, images, steps):
		numVertical, numHorizontal, height, width, channels = images.shape
		video = cv2.VideoWriter(fileName, cv2.cv.CV_FOURCC(*'MJPG'), 15, (width, height))
		frames = []
		for displacement in steps:
			print displacement
			frame = LightField.displace(images, displacement)
			frame = LightField.merge(frame, 4)
			frame = Normalizer.to8bit(frame)
			frames.append(frame.clip(0, 255).astype(np.uint8))

		for frame in itertools.chain(frames,reversed(frames)):
			video.write(frame)

		video.release()