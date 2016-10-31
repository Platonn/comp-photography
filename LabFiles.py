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
			2: {
				'sec1-1': 'sec1/_MG_4460.tiff',
				'sec1-2': 'sec1/_MG_4461.tiff',
				'sec1-3': 'sec1/_MG_4462.tiff',
				'sec3-1': 'sec3/_MG_4469.resized.tiff',
				'sec3-2': 'sec3/_MG_4470.resized.tiff',
				'sec3-3': 'sec3/_MG_4471.resized.tiff'
			},
			3: {
				'exr': 'Memorial_SourceImages/memorial.exr'
			}
		}
	}

	EXPOSURE_TIMES = {
		2: {
			2: {
				'sec3-1': 0.2,
				'sec3-2': 0.05,
				'sec3-3': 0.8,
			}
		}
	}

	@staticmethod
	def input(listNum, taskNum, name):
		return LabFiles.ROOT_PATH + str(listNum) + '/in/' + LabFiles.IN_FILENAMES[listNum][taskNum][name]

	@staticmethod
	def output(listNum, taskNum, name, ext='.png'):
		return LabFiles.ROOT_PATH + str(listNum) + '/out/' + str(listNum) + '.' + str(taskNum) + '.' + name + ext

	@staticmethod
	def show(listNum, taskNum, name, ext='.png'):
		os.system("xdg-open " + LabFiles.output(listNum, taskNum, name, ext))

	@staticmethod
	def exposureTime(listNum, taskNum, name):
		return LabFiles.EXPOSURE_TIMES[listNum][taskNum][name]