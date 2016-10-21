import time


class Timer:
	items = {}

	@staticmethod
	def start(name):
		Timer.items[name] = time.time()
		print "timer " + name

	@staticmethod
	def stop(name):
		result = time.time() - Timer.items[name]
		del Timer.items[name]
		print "timer " + name + ": %.3f" % result
		return result
