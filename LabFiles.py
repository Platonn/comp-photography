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
				'sec3-1':            'sec3/_MG_4469-16bit.resized.tiff',
				'sec3-2':            'sec3/_MG_4470-16bit.resized.tiff',
				'sec3-3':            'sec3/_MG_4471-16bit.resized.tiff',

				'sec3-1-16bit-srgb': 'sec3/_MG_4469-16bit-sRGB.resized.tiff',
				'sec3-2-16bit-srgb': 'sec3/_MG_4470-16bit-sRGB.resized.tiff',
				'sec3-3-16bit-srgb': 'sec3/_MG_4471-16bit-sRGB.resized.tiff',

				'memorial-1':        'Memorial_SourceImages/memorial0061.png',
				'memorial-2':        'Memorial_SourceImages/memorial0062.png',
				'memorial-3':        'Memorial_SourceImages/memorial0063.png',
				'memorial-4':        'Memorial_SourceImages/memorial0064.png',
				'memorial-5':        'Memorial_SourceImages/memorial0065.png',
				'memorial-6':        'Memorial_SourceImages/memorial0066.png',
				'memorial-7':        'Memorial_SourceImages/memorial0067.png',
				'memorial-8':        'Memorial_SourceImages/memorial0068.png',
				'memorial-9':        'Memorial_SourceImages/memorial0069.png',
				'memorial-10':       'Memorial_SourceImages/memorial0070.png',
				'memorial-11':       'Memorial_SourceImages/memorial0071.png',
				'memorial-12':       'Memorial_SourceImages/memorial0072.png',
				'memorial-13':       'Memorial_SourceImages/memorial0073.png',
				'memorial-14':       'Memorial_SourceImages/memorial0074.png',
				'memorial-15':       'Memorial_SourceImages/memorial0075.png',
				'memorial-16':       'Memorial_SourceImages/memorial0076.png',

			},
			3: {
				'exr': 'Memorial_SourceImages/memorial.exr'
			}
		},
		3: {
			1: {
				'green':  'green.png',
				'poster': 'poster.png'
			},
			2: {
				'green':  'green.png',
				'poster': 'poster.png'
			},
			3: {
				'green':  'green.png',
				'poster': 'poster.png',
				'stata-1': 'pano/stata-1.png',
				'stata-2': 'pano/stata-2.png'
			}
		}
	}

	EXPOSURE_TIMES = {
		2: {
			2: {
				'sec3-1':      0.2,
				'sec3-2':      0.05,
				'sec3-3':      0.8,
				'memorial-1':  1.0 / 0.03125,
				'memorial-2':  1.0 / 0.0625,
				'memorial-3':  1.0 / 0.125,
				'memorial-4':  1.0 / 0.25,
				'memorial-5':  1.0 / 0.5,
				'memorial-6':  1.0,
				'memorial-7':  1.0 / 2.0,
				'memorial-8':  1.0 / 4.0,
				'memorial-9':  1.0 / 8.0,
				'memorial-10': 1.0 / 16.0,
				'memorial-11': 1.0 / 32.0,
				'memorial-12': 1.0 / 64.0,
				'memorial-13': 1.0 / 128.0,
				'memorial-14': 1.0 / 256.0,
				'memorial-15': 1.0 / 512.0,
				'memorial-16': 1.0 / 1024.0
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