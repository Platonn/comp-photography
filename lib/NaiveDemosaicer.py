from Demosaicer import *

class NaiveDemosaicer(Demosaicer):
	def run(self):
		self.__runRed()


	def __runRed(self):
		im = self.tempImage
		s = 2 #shift
		c = 2 #olor

		im[1:-2:s, 2:-1:s, c] = (im[1:-2:s, 1:-2:s, c] + im[1:-2:s, 3::s, c]) / 2 # left right
		im[2:-1:s, 1:-2:s, c] += (im[1:-2:s, 1:-2:s, c] + im[3::s, 1:-2:s, c]) / 2 # up down

		im[2:-1:s, 2:-1:s, c] = (
			im[1:-2:s, 1:-2:s, c] +
			im[1:-2:s, 3::s, c] +
			im[3::s, 1:-2:s, c] +
			im[3::s, 3::s, c]
		) /4

	def __runBlue(self):
		pass


	# def demosaic(self):
	# 	self.demosaic_color('r')
	# 	self.demosaic_color('g')
	# 	self.demosaic_color('b')
	#
	# def demosaic_color(self, color):
	# 	for x in range(0, self.image.width):
	# 		for y in range(0, self.image.height):
	# 			filter_schema = self.get_filter_schema(x, y, color)
	# 			self.apply_filter(x, y, self.monochrom_images[color], filter_schema)
