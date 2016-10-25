from Demosaicer import *
from utils.Uint8Util import *


class EdgeAwareDemosaicer(Demosaicer):
	def run(self):
		self.__runGreen()
		self.__runRedAndBlue()

	def __runGreen(self):
		im = self.tempImage
		(height, width, channels) = im.shape
		c = 1  # color

		for y in range(1, height - 1):  # exclude last
			for x in range(1, width - 1):  # exclude last

				# interpolate not-green
				if x % 2 == y % 2:  # shift - only diagonal and analogical
					left = int(im[y, x - 1, c])
					right = int(im[y, x + 1, c])
					top = int(im[y - 1, x, c])
					bottom = int(im[y + 1, x, c])
					dH = abs(left - right)
					dV = abs(top - bottom)

					if dH < dV:
						newValue = (left + right) / 2
					elif dH > dV:
						newValue = (top + bottom) / 2
					else:
						newValue = (top + bottom + left + right) / 4

					im[y, x, c] = newValue

	def __runRedAndBlue(self):
		im = self.tempImage
		(height, width, channels) = im.shape
		b=0
		r = 2
		g = 1
		for y in range(1, height - 1):  # exclude last
			for x in range(1, width - 1):  # exclude last

				# interpolate RED:
				topLef = int(im[y - 1, x - 1, r]) - int(im[y - 1, x - 1, g])
				topRig = int(im[y - 1, x + 1, r]) - int(im[y - 1, x + 1, g])
				botLef = int(im[y + 1, x - 1, r]) - int(im[y + 1, x - 1, g])
				botRig = int(im[y + 1, x + 1, r]) - int(im[y + 1, x + 1, g])
				top = int(im[y - 1, x, r]) - int(im[y - 1, x, g])
				bot = int(im[y + 1, x, r]) - int(im[y + 1, x, g])
				rig = int(im[y, x + 1, r]) - int(im[y, x + 1, g])
				lef = int(im[y, x - 1, r]) - int(im[y, x - 1, g])
				cent = int(im[y, x, r]) - int(im[y, x, g])

				greenVal = im[y, x, g]

				if y % 2 == x % 2 and y % 2 == 0:  # blue
					naiveInterpolation = (topLef + botRig + topRig + botLef) / 4

				elif y % 2 == 1 and x % 2 == 0:  # green1
					naiveInterpolation = (lef + rig) / 2

				elif y % 2 == 0 and x % 2 == 1:  # green2
					naiveInterpolation = (top + bot) / 2

				else:
					naiveInterpolation = cent

				result = naiveInterpolation + greenVal
				im[y, x, r] = Uint8Util.constrain(result)

				# interpolate BLUE:
				topLef = int(im[y - 1, x - 1, b]) - int(im[y - 1, x - 1, g])
				topRig = int(im[y - 1, x + 1, b]) - int(im[y - 1, x + 1, g])
				botLef = int(im[y + 1, x - 1, b]) - int(im[y + 1, x - 1, g])
				botRig = int(im[y + 1, x + 1, b]) - int(im[y + 1, x + 1, g])
				top = int(im[y - 1, x, b]) - int(im[y - 1, x, g])
				bot = int(im[y + 1, x, b]) - int(im[y + 1, x, g])
				rig = int(im[y, x + 1, b]) - int(im[y, x + 1, g])
				lef = int(im[y, x - 1, b]) - int(im[y, x - 1, g])
				cent = int(im[y, x, b]) - int(im[y, x, g])

				greenVal = im[y, x, g]

				if y % 2 == x % 2 and y % 2 == 1:  # red
					naiveInterpolation = (topLef + botRig + topRig + botLef) / 4
				elif y % 2 == 1 and x % 2 == 0:  # green1
					naiveInterpolation = (top + bot) / 2
				elif y % 2 == 0 and x % 2 == 1:  # green2
					naiveInterpolation = (lef + rig) / 2
				else:
					naiveInterpolation = cent

				result = naiveInterpolation + greenVal
				im[y, x, b] = Uint8Util.constrain(result)
