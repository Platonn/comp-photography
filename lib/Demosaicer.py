import cv2
import numpy as np


class Demosaicer:
	def __init__(self, rawImage):
		self.rawImage = rawImage
		self.tempImage = cv2.copyMakeBorder(self.rawImage, 1, 1, 1, 1, cv2.BORDER_REFLECT_101)
		self.outImage = rawImage.copy()

	def saveOutput(self, fileName):
		self.__temp2output()
		cv2.imwrite(fileName, self.outImage)

	def __temp2output(self):
		self.outImage[:, :] = self.tempImage[1:-1, 1:-1]


# from PIL import Image
#
# from lib.BayerPattern import BayerPattern
# from lib.utils.TupleUtil import TupleUtil
#
#
# class Demosaicer:
# 	UNIT_COLORS = {
# 		'r': (1, 0, 0),
# 		'g': (0, 1, 0),
# 		'b': (0, 0, 1)
# 	}
#
# 	def __init__(self, image_in):
# 		self.image = image_in
# 		self.monochrom_images = {
# 			'r': Image.new('L', (image_in.width, image_in.height)),
# 			'g': Image.new('L', (image_in.width, image_in.height)),
# 			'b': Image.new('L', (image_in.width, image_in.height))
# 		}
# 		self.image_out = Image.new('RGB', (image_in.width, image_in.height))
#
# 	# self.load_rgb(image_in) #spike
#
# 	def load_rgb(self):
# 		image_in = self.image
# 		for x in range(0, image_in.width):
# 			for y in range(0, image_in.height):
# 				brightness_in = image_in.getpixel((x, y))
# 				bayer_color_tuple = self.get_colors_tuple_by_bayer_position(x, y)
# 				(r, g, b) = TupleUtil.mult_by_scalar(bayer_color_tuple, brightness_in)
# 				self.monochrom_images['r'].putpixel((x, y), r)
# 				self.monochrom_images['g'].putpixel((x, y), g)
# 				self.monochrom_images['b'].putpixel((x, y), b)
# 				self.image_out.putpixel((x, y), (r, g, b))
#
# 	def get_colors_tuple_by_bayer_position(self, x, y):
# 		return self.UNIT_COLORS[BayerPattern.COLOR[y % 2][x % 2]]
#
# 	def show(self):
# 		self.image_out.show()
#
# 	def save(self, filename):
# 		self.image_out.save(filename)
#
# 	def isOutOfBound(self, x, y):
# 		return (
# 			x < 0 or x > self.image.width or
# 			y < 0 or y > self.image.height
# 		)
#
# 	def getpixel_smart(self, x, y, image):  # serves edge-mirrored pixels if asked for out of bounds indexes
# 		width = image.width
# 		height = image.height
# 		if x < 0: x = -x
# 		if y < 0: y = -y
# 		if x >= width: x = 2 * width - x - 1
# 		if y >= height: y = 2 * height - y - 1
# 		return self.image.getpixel((x, y))
#
# 	def get_nine_neighbour_pixels_smart(self, x, y, image):
# 		# aliases for good readability:
# 		f = self.getpixel_smart
# 		i = image
# 		return [
# 			[f(x - 1, y - 1, i), f(x + 0, y - 1, i), f(x + 1, y - 1, i)],
# 			[f(x - 1, y + 0, i), f(x + 0, y + 0, i), f(x + 1, y + 0, i)],
# 			[f(x - 1, y + 1, i), f(x + 0, y + 1, i), f(x + 1, y + 1, i)]
# 		]
#
# 	def apply_filter(self, x, y, image, filter_schema):
# 		neighbours = self.get_nine_neighbour_pixels_smart(x, y, image)
# 		for i in range(0, 3):
# 			for j in range(0, 3):
# 				new_value = neighbours[j][i] * filter_schema[j][i]
# 				image.putpixel((x, y), new_value)
#
# 	def get_filter_schema(self, x, y, color):
# 		filter_name = BayerPattern.FILTERS[color][y % 2][x % 2]
# 		filter_schema = BayerPattern.FILTER_SCHEMA[filter_name]
# 		return filter_schema
#
# 	def merge_monochrom_images(self):
# 		# SPIKE - mozna optymalniej! z kazdego getdata i potem zip na tuplach! a potem putdata
# 		for x in range(0, self.image.width):
# 			for y in range(0, self.image.height):
# 				r = self.monochrom_images['r'].getpixel((x, y))
# 				g = self.monochrom_images['g'].getpixel((x, y))
# 				b = self.monochrom_images['b'].getpixel((x, y))
# 				self.image_out.putpixel((x, y), (r, g, b))
