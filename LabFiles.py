import os

class LabFiles:
	def __init__(self):
		pass

	ROOT_PATH = '../'

	IN_FILENAMES = {
		1: {
			1: {
				'raw': 'lighthouse_RAW_noisy_sigma0.01.png'
			},
			2: {
				'raw': 'lighthouse_RAW_noisy_sigma0.01.png'
			}
		},
	}

	@staticmethod
	def input(listNum, taskNum, name):
		return LabFiles.ROOT_PATH + str(listNum) + '/in/' + LabFiles.IN_FILENAMES[listNum][taskNum][name]

	@staticmethod
	def output(listNum, taskNum, name):
		return LabFiles.ROOT_PATH + str(listNum) + '/out/' + str(listNum) + '.' + str(taskNum) + '.' + name + '.png'

	@staticmethod
	def show(listNum, taskNum, name):
		os.system("xdg-open " + LabFiles.output(listNum, taskNum, name))
