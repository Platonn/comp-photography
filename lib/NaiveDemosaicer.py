from Demosaicer import Demosaicer
from BayerPattern import BayerPattern


class NaiveDemosaicer(Demosaicer):
	def demosaic(self):
		self.demosaic_color('r')
		self.demosaic_color('g')
		self.demosaic_color('b')

	def demosaic_color(self, color):
		for x in range(0, self.image.width):
			for y in range(0, self.image.height):
				filter_schema = self.get_filter_schema(x, y, color)
				self.apply_filter(x, y, self.monochrom_images[color], filter_schema)
