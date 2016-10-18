from PIL import Image


class Demosaicer:
	BAYER_PATTERN_COLOR = [
		[(1, 0, 0), (0, 1, 0)],  # RG
		[(0, 1, 0), (0, 0, 1)],  # GB
	]

	def __init__(self, image_in):
		self.image_in = image_in
		self.image_out = Image.new('RGB', (self.image_in.width, self.image_in.height))
		self.__load_rgb()

	def __load_rgb(self):
		for x in range(0, self.image_in.width):
			for y in range(0, self.image_in.height):
				brightness_in = self.image_in.getpixel((x, y))
				bayer_color_tuple = self.__get_colors_tuple_by_bayer_position(x, y)
				color = tuple(brightness_in * value for value in bayer_color_tuple)
				self.image_out.putpixel((x, y), color)

	def __get_colors_tuple_by_bayer_position(self, x, y):
		return self.BAYER_PATTERN_COLOR[x % 2][y % 2]

	def show(self):
		self.image_out.show()