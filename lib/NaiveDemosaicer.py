from Demosaicer import *


class NaiveDemosaicer(Demosaicer):
	def run(self):
		self.zeroProperColors()

		self.__runRed()
		self.__runBlue()
		self.__runGreen()

	def zeroProperColors(self):
		im = self.tempImage
		b = 0
		g = 1
		r = 2
		s = 2  # shift
		# (B) (G) (B)
		# (G)  R   G
		# (B)  G   B

		# (B)
		#
		im[0::s, 0::s, g] = 0
		im[0::s, 0::s, r] = 0

		#     (G)
		#
		im[0::s, 1::s, b] = 0
		im[0::s, 1::s, r] = 0

		#
		# (G)
		im[1::s, 0::s, b] = 0
		im[1::s, 0::s, r] = 0

		#
		#      R
		im[1::s, 1::s, b] = 0
		im[1::s, 1::s, g] = 0

	def __runRed(self):
		im = self.tempImage
		s = 2  # shift
		c = 2  # color

		im[1:-2:s, 2:-1:s, c] = im[1:-2:s, 1:-2:s, c] / 2 + im[1:-2:s, 3::s, c] / 2  # left right
		im[2:-1:s, 1:-2:s, c] = im[1:-2:s, 1:-2:s, c] / 2 + im[3::s, 1:-2:s, c] / 2  # up down

		im[2:-1:s, 2:-1:s, c] = (
			im[1:-2:s, 1:-2:s, c] / 4 +
			im[1:-2:s, 3::s, c] / 4 +
			im[3::s, 1:-2:s, c] / 4 +
			im[3::s, 3::s, c] / 4
		)

	def __runBlue(self):
		im = self.tempImage
		s = 2  # shift
		c = 0  # color

		im[1:-2:s, 1:-2:s, c] = (
			im[0:-3:s, 0:-3:s, c] / 4 +
			im[0:-3:s, 2:-1:s, c] / 4 +
			im[2:-1:s, 0:-3:s, c] / 4 +
			im[2:-1:s, 2:-1:s, c] / 4
		)

		im[1:-2:s, 2:-1:s, c] = im[0:-3:s, 2:-1:s, c] / 2 + im[2:-1:s, 2:-1:s, c] / 2
		im[2:-1:s, 1:-2:s, c] = im[2:-1:s, 0:-3:s, c] / 2 + im[2:-1:s, 2:-1:s, c] / 2

	def __runGreen(self):
		im = self.tempImage
		s = 2  # shift
		c = 1  # color

		im[1:-2:s, 1:-2:s, c] = (
			im[0:-3:s, 1:-2:s, c] / 4 +
			im[1:-2:s, 0:-3:s, c] / 4 +
			im[2:-1:s, 1:-2:s, c] / 4 +
			im[1:-2:s, 2:-1:s, c] / 4
		)

		im[2:-1:s, 2:-1:s, c] = (
			im[1:-2:s, 2:-1:s, c] / 4 +
			im[2:-1:s, 1:-2:s, c] / 4 +
			im[2:-1:s, 3::s, c] / 4 +
			im[3::s, 2:-1:s, c] / 4
		)

