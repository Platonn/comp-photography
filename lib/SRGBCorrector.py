import numpy as np

# Used equations from: http://entropymine.com/imageworsener/srgbformula/
class SRGBCorrector:
	CURVE_BREAKPOINT = 0.03928

	@staticmethod
	def apply_inversed_sRGB(image):
		apply_sRGB_vectorized = np.vectorize(SRGBCorrector.__apply_inversed_sRGB_local)
		return apply_sRGB_vectorized(image)

	@staticmethod
	def __apply_inversed_sRGB_local(value):
		if (value <= SRGBCorrector.CURVE_BREAKPOINT):
			return value / 12.92
		else:
			return ((value + 0.055) / 1.055) ** 2.4

