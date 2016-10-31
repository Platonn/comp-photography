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
			},
			3: {
				'raw': 'lighthouse_RAW_noisy_sigma0.01.png'
			},
			5: {
				'raw': 'raw/_MG_4257.tiff'
			}
		},
		2: {
			1: {
				'stack-1': 'focalstack/stack1.png',
				'stack-2': 'focalstack/stack2.png',
				'stack-3': 'focalstack/stack3.png',
			},
			3: {
				'exr': 'Memorial_SourceImages/memorial.exr'
			}
		}
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
