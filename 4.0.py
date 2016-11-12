import cv2
from LabFiles import *
from lib.utils.Timer import *
from lib.Homography import *
from lib.HomographyFinder import *
import os
import scipy.misc
import pprint

pp = pprint.PrettyPrinter(indent=4)


def applyFunctionToFiles(customFunction, functionName, inFolder, suffix, feedbackObject=None):
	stoperName = functionName + ' ' + inFolder
	Timer.start(stoperName)
	for fileName in sorted(os.listdir(inFolder)):
		if fileName.endswith(suffix):
			customFunction(inFolder, fileName, feedbackObject)
	Timer.stop(stoperName)


def getDir(target, subFolder=''):
	if subFolder != '': subFolder += '/'
	return '../4/in/' + target + 'set/' + subFolder


def filesGetResizedFullDescriptor(target):
	feedbackObject = {
		'fileNames': ['zeros'],
		'descriptors': np.zeros(32*32)
	}

	def get32Descriptor(inFolder, fileName, feedbackObject):
		im = cv2.imread(inFolder + fileName, cv2.IMREAD_GRAYSCALE)
		descriptor = im.flatten()

		feedbackObject['fileNames'].append(fileName)
		feedbackObject['descriptors'] = np.vstack((feedbackObject['descriptors'], descriptor))

	applyFunctionToFiles(get32Descriptor, 'get32Descriptor', getDir(target, 'resized'), '.jpg')
	np.save(getDir(target, 'resized') + 'descriptors32.npy', feedbackObject)

def filesResizeTo32(target):
	def resize32(inFolder, fileName, feedbackObject):
		im = cv2.imread(inFolder + fileName)
		result = cv2.resize(im, (32, 32))
		cv2.imwrite(getDir(target, 'resized') + fileName, result)

	applyFunctionToFiles(resize32, 'resize32', getDir(target), '.jpg')


# spike function
def countFiles(target):
	feedbackObject = {'counter': 0}

	def count(inFolder, fileName, feedbackObject):
		feedbackObject['counter'] += 1

	applyFunctionToFiles(count, 'count', getDir(target), '.jpg', feedbackObject)
	print "number of files: " + str(feedbackObject['counter'])


def filesCalculateSSD(target, descriptorType, testDescriptor):
	feedbackObject = {
		'testDescriptor': testDescriptor,
		'ssdValues':      []
	}

	def calculateSSD(inFolder, fileName, feedbackObject):
		testDescriptor = feedbackObject['testDescriptor']
		comparedDescriptor = np.load(inFolder + fileName)
		ssdValue = np.sum((testDescriptor - comparedDescriptor) ** 2)
		feedbackObject['ssdValues'].append({
			'fileName': fileName,
			'value':    ssdValue
		})

	applyFunctionToFiles(calculateSSD, 'calculateSSD', getDir(target, 'resized'), descriptorType + '.npy', feedbackObject)
	pp.pprint(feedbackObject)


def filesCalculatePCABase(target):
	feedbackObject = {
		'descriptorsEmpty': True,
		'descriptors':      np.array([]),
	}

	def calculatePCABase(inFolder, fileName, feedbackObject):
		descriptor = np.load(inFolder + fileName)
		if feedbackObject['descriptorsEmpty']:
			feedbackObject['descriptorsEmpty'] = False
			feedbackObject['descriptors'] = np.array(descriptor)
		else:
			feedbackObject['descriptors'] = np.vstack(
				(feedbackObject['descriptors'], descriptor))  # works only if array has any rows

	applyFunctionToFiles(calculatePCABase, 'calculatePCABase', getDir(target, 'resized'), '.desc32.npy',
	                     feedbackObject)
	descriptors = feedbackObject['descriptors']
	PCABase = cv2.PCACompute(descriptors, maxComponents=19)  # (meanPCA, eigenvectorsPCA)
	np.save(getDir(target, 'resized') + 'PCABase.npy', PCABase)


def filesGetResizedPCADescriptor(target):
	feedbackObject = {'PCABase': np.load(getDir(target, 'resized') + 'PCABase.npy')}

	def getResizedPCADescriptor(inFolder, fileName, feedbackObject):
		print fileName
		meanPCA, eigenvectorsPCA = feedbackObject['PCABase']
		descriptor32 = np.load(inFolder + fileName)
		descriptorPCA = cv2.PCAProject(np.array([descriptor32]), meanPCA, eigenvectorsPCA)
		np.save(inFolder + fileName + '.descPCA.npy', descriptorPCA)

	applyFunctionToFiles(getResizedPCADescriptor, 'getResizedPCADescriptor', getDir(target, 'resized'), '.desc32.npy', feedbackObject)

def getColorFromImage(inFolder, inFileName, outFolder, outFileName):
	# otworzyc obrazek IN i OUT
	# przekonwertowac IN i OUT na YCrCb
	# przekopiowac Cr i Cb ([1] i [2] kanaL) z IN do OUT
	# skonwertowac OUT do RGB, zapisac OUT
	pass


def main():
	filesResizeTo32('test')
	filesGetResizedFullDescriptor('test')
	filesCalculatePCABase('test')
	filesGetResizedPCADescriptor('test')

	# testDescriptor = np.load(getDir('test', 'resized') + '1.jpg.descPCA.npy')  # spike
	# filesCalculateSSD('test', '.descPCA', testDescriptor)


#   spike - sprawdzenie czy dziala filesCalculateSSD:
# testDescriptor = np.load(getDir('test', 'resized') + '21.jpg.desc32.npy')  # spike
# filesCalculateSSD('test', '.desc32', testDescriptor)

Timer.start('program')
main()
Timer.stop('program')