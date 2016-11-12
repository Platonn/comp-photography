import time


class Timer:
	items = {}

	INDENTS = 0
	INDENT_SYMBOL = ''
	@staticmethod
	def start(name):
		Timer.items[name] = time.time()
		print (Timer.INDENTS * Timer.INDENT_SYMBOL) + "timer " + name
		Timer.INDENTS +=1

	@staticmethod
	def stop(name):
		result = time.time() - Timer.items[name]
		del Timer.items[name]
		Timer.INDENTS -= 1
		print (Timer.INDENTS * Timer.INDENT_SYMBOL) + "timer " + name + ": %.3f" % result
		return result
