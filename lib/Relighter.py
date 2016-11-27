import numpy as np
import sys
from math import cos, sin, sqrt, acos, pi
from lib.utils.Timer import *

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
		Timer.start('relightImage')
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
		Timer.stop('relightImage')
		return result
