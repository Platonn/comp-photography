import cv2
import numpy as np


class BilateralFilterToneMapper:
	@staticmethod
	def run(imExr, d = -1, sigmaColor = 0.5, sigmaSpace= 10, targetContrastParam=5):
		im = imExr
		B = im[:, :, 0]
		G = im[:, :, 1]
		R = im[:, :, 2]

		# 1
		inputIntensity = 1.0 / 61.0 * (20.0 * R + 40.0 * G + B)

		# 2
		r = R / inputIntensity
		g = G / inputIntensity
		b = B / inputIntensity

		# 3
		logInputIntensity = np.log10(inputIntensity)
		logBase = cv2.bilateralFilter(logInputIntensity, d, sigmaColor, sigmaSpace)

		# 4
		logDetail = logInputIntensity - logBase

		# 5_
		targetContrast = np.log10(targetContrastParam)
		maxLogBase = np.max(logBase)
		minLogBase = np.min(logBase)
		compressionFactor = targetContrast / (maxLogBase - minLogBase)
		logAbsoluteScale = maxLogBase * compressionFactor
		# 5
		logOutputIntensity = logBase * compressionFactor + logDetail - logAbsoluteScale

		# 6
		power10logOutputIntensity = np.power(10, logOutputIntensity)
		R_output = r * power10logOutputIntensity
		G_output = g * power10logOutputIntensity
		B_output = b * power10logOutputIntensity

		result = np.zeros(im.shape)
		result[:, :, 0] = B_output
		result[:, :, 1] = G_output
		result[:, :, 2] = R_output

		#spike:
		result *= 255

		return result