
class Uint8Util:
	@staticmethod
	def constrain(value):
		return min(max(value,0), 255)