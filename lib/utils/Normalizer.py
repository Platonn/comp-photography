import cv2
import numpy as np


class Normalizer:
	MAX_16_BIT = 65535
	MAX_8_BIT = 255

	@staticmethod
	def from16bit(image):
		return image.astype('float32') / Normalizer.MAX_16_BIT

	@staticmethod
	def from8bit(image):
		return image.astype('float32') / Normalizer.MAX_8_BIT

	@staticmethod
	def to8bit(image):
		return image * Normalizer.MAX_8_BIT

	@staticmethod
	def normalize(image):
		return image / np.max(image)
