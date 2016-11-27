import numpy as np
import sys
from math import cos, sin, sqrt, acos, pi
import cv2

from lib.utils.Normalizer import *
from utils.Timer import *


class Relighter:
	EPSILON = sys.float_info.epsilon

	@staticmethod
	def deg2rad((phi, theta)):
		return float(np.deg2rad(phi)), float(np.deg2rad(theta))

	@staticmethod
	def thetaPhi2DxDyDz((theta, phi)):
		Dx = cos(phi) * sin(theta)
		Dy = -sin(phi)
		Dz = -cos(phi) * cos(theta)
		return Dx, Dy, Dz

	@staticmethod
	def DxDyDz2UV((Dx, Dy, Dz)):
		# handle sqrt(Dx ** 2 + Dy ** 2) == 0 ->dividing by zero
		# denomiantor = sqrt(Dx ** 2 + Dy ** 2)
		if abs(Dx) <= Relighter.EPSILON and abs(Dy) <= Relighter.EPSILON:
			if Dz > 0:  # looking to me
				result = (0, -1)  # get any point from circuit, eg. (0,-1)
			else:  # looking from me
				result = (0, 0)  # get point from center
		else:
			r = (1. / pi) * acos(-Dz) / sqrt(Dx ** 2 + Dy ** 2)
			result = (Dx * r, Dy * r)
		# print result
		return result

	@staticmethod
	def UV2ProbeUV((u, v), probeHeight, probeWidth):
		resU = (u + 1.0) * probeHeight / 2.0
		resV = (v + 1.0) * probeWidth / 2.0
		return int(resU), int(resV)

	@staticmethod
	def relightImage(images, dirs, intens, probe):  # images, directions, intensities
		# Timer.start('relightImage')
		result = np.zeros(images[0].shape)
		probeHeight, probeWidth, _ = probe.shape

		for i in range(0, len(images)):
			# print i
			im = images[i]
			dir = dirs[i]
			intensity = intens[i]
			UV = Relighter.DxDyDz2UV(dir)
			probeU, probeV = Relighter.UV2ProbeUV(UV, probeHeight, probeWidth)
			result += im * probe[probeV, probeU] * intensity  ## SPIKE - uwaga: najpierw V, a potem U
		# Timer.stop('relightImage')
		return result

	@staticmethod
	def relightVideo(videoFileName, framesNumber, videoDuration, images, dirs, intens, probe):
		Timer.start('relightVideo')
		fps = int(float(framesNumber) / float(videoDuration))

		height, width, _ = images[0].shape
		video = cv2.VideoWriter(videoFileName, cv2.cv.CV_FOURCC(*'MJPG'), fps, (width, height))

		# framesNumber = 10
		for i in range(framesNumber):
			print i
			angle = 2.0 * pi * (float(i) / framesNumber)
			rotationMatrix = Relighter.yRotationMatrix(angle)
			rotatedDirs = [np.dot(rotationMatrix, direction) for direction in dirs]
			relightedIm = Relighter.relightImage(images, rotatedDirs, intens, probe)
			relightedIm = Normalizer.normalize(relightedIm)
			relightedIm = Normalizer.to8bit(relightedIm)
			video.write(relightedIm.astype(np.uint8))
		Timer.stop('relightVideo')
		Timer.start('releaseVideo')
		video.release()
		Timer.stop('releaseVideo')

	@staticmethod
	def yRotationMatrix(x):
		return [
			[cos(x), 0., sin(x)],
			[0., 1., 0.],
			[-sin(x), 0., cos(x)]
		]

	@staticmethod
	def xRotationMatrix(x):
		return [
			[1., 0., 0.],
			[0., cos(x), -sin(x)],
			[0., sin(x), cos(x)]
		]

	@staticmethod
	def zRotationMatrix(x):
		return [
			[cos(x), -sin(x), 0.],
			[sin(x), cos(x), 0.],
			[0., 0., 1.]
		]