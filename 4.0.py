import cv2
from LabFiles import *
from lib.utils.Timer import *
from lib.Homography import *
from lib.HomographyFinder import *
import os


def applyFunctionToFiles(customFunction, functionName, inFolder, suffix, feedbackObject=None):
	stoperName = functionName + ' ' + inFolder
	Timer.start(stoperName)
	for fileName in sorted(os.listdir(inFolder)):
		if fileName.endswith(suffix):
			customFunction(inFolder, fileName, feedbackObject)
	Timer.stop(stoperName)


def getDir(target, subFolder=''):
	if subFolder != '': subFolder += '/'
	return '../4/in/' + target + '/' + subFolder


def filesGet32x32Descriptor(target):
	feedbackObject = {
		'fileNames':        [],
		'descriptors32x32': []
	}

	def get32x32Descriptor(inFolder, fileName, feedbackObject):
		im = cv2.imread(inFolder + fileName, cv2.IMREAD_GRAYSCALE)
		descriptor = im.flatten()

		feedbackObject['fileNames'].append(fileName)
		feedbackObject['descriptors32x32'].append(descriptor)

	applyFunctionToFiles(get32x32Descriptor, 'get32x32Descriptor', getDir(target, 'resized'), '.jpg', feedbackObject)

	Timer.start('filesGet32x32Descriptor vstack')
	feedbackObject['descriptors32x32'] = np.vstack(feedbackObject['descriptors32x32'])
	Timer.stop('filesGet32x32Descriptor vstack')

	Timer.start('filesGet32x32Descriptor save descriptors32x32')
	np.save(getDir(target, 'resized') + 'descriptors32x32.npy', feedbackObject['descriptors32x32'])
	Timer.stop('filesGet32x32Descriptor save descriptors32x32')

	Timer.start('filesGet32x32Descriptor save fileNames')
	np.save(getDir(target, 'resized') + 'fileNames.npy', feedbackObject['fileNames'])
	Timer.stop('filesGet32x32Descriptor save fileNames')


def filesResizeTo32(target):
	def resize32(inFolder, fileName, feedbackObject):
		im = cv2.imread(inFolder + fileName)
		result = cv2.resize(im, (32, 32))
		cv2.imwrite(getDir(target, 'resized') + fileName, result)

	applyFunctionToFiles(resize32, 'resize32', getDir(target), '.jpg')


def calculateSSD(target, descriptorsFileName, testDescriptor):
	# Timer.start('calculateSSD')
	descriptors = np.load(descriptorsFileName)
	testDescriptorMatrix = np.zeros(descriptors.shape)
	testDescriptorMatrix[...] = testDescriptor

	def ssdPerRow(descriptorsRow, testDescriptor):
		return np.sum((descriptorsRow - testDescriptor) ** 2)

	ssdValues = np.apply_along_axis(ssdPerRow, 1, descriptors, testDescriptor)
	minSsdValue = np.min(ssdValues)
	minSsdValueIndex = np.argmin(ssdValues)
	# print minSsdValue
	# Timer.stop('calculateSSD')
	return (minSsdValue, minSsdValueIndex)


def calculatePCABase(target, maxComponents):
	Timer.start('calculatePCABase')

	Timer.start('calculatePCABase load descriptors32x32')
	descriptors32x32 = np.load(getDir(target, 'resized') + 'descriptors32x32.npy')
	Timer.stop('calculatePCABase load descriptors32x32')

	Timer.start('calculatePCABase PCACompute')
	PCABase = cv2.PCACompute(descriptors32x32, maxComponents=maxComponents)  # (meanPCA, eigenvectorsPCA)
	Timer.stop('calculatePCABase PCACompute')

	np.save(getDir(target, 'resized') + str(maxComponents) + 'PCABase.npy', PCABase)
	Timer.stop('calculatePCABase')


def getPCADescriptors(target, PCABaseFileName, maxComponents):
	Timer.start('getPCADescriptors')
	PCABase = np.load(PCABaseFileName)
	meanPCA, eigenvectorsPCA = PCABase
	descriptors32x32 = np.load(getDir(target, 'resized') + 'descriptors32x32.npy')
	descriptorsPCA = cv2.PCAProject(descriptors32x32, meanPCA, eigenvectorsPCA)
	np.save(getDir(target, 'resized') + str(maxComponents) + 'descriptorsPCA.npy', descriptorsPCA)
	Timer.stop('getPCADescriptors')


def getDescriptor(target, descriptorsFileName, fileName):
	fileNames = np.load(getDir(target, 'resized') + 'fileNames.npy')
	descriptors = np.load(descriptorsFileName)
	index = np.where(fileNames == fileName)
	descriptor = descriptors[index]
	result = descriptor[0]
	return result


def copyColorBetweenImages(colorFileName, grayFileName, outputFileName):
	colorIm = cv2.imread(colorFileName)
	grayIm = cv2.imread(grayFileName)

	if (colorIm.shape != grayIm.shape):
		print 'images shapes dont match (applied resizing)'
		colorIm = cv2.resize(colorIm, (grayIm.shape[1], grayIm.shape[0]))

	colorIm = cv2.cvtColor(colorIm, cv2.COLOR_BGR2YCR_CB)
	grayIm = cv2.cvtColor(grayIm, cv2.COLOR_BGR2YCR_CB)
	grayIm[:, :, 1:] = colorIm[:, :, 1:]  # copy CrCb channels
	grayIm = cv2.cvtColor(grayIm, cv2.COLOR_YCR_CB2BGR)
	cv2.imwrite(outputFileName, grayIm)


def copyImage(inFileName, outFileName):
	os.system('cp ' + inFileName + ' ' + outFileName)


### PREPARE DATA:

def prepare_resized():
	filesResizeTo32('testset')
	filesResizeTo32('trainset')


def prepare_descriptors32():
	filesGet32x32Descriptor('testset')
	filesGet32x32Descriptor('trainset')


def prepare_descriptorsPCA(maxComponents):
	calculatePCABase('trainset', maxComponents)
	getPCADescriptors('trainset', getDir('trainset', 'resized') + str(maxComponents) + 'PCABase.npy', maxComponents)
	getPCADescriptors('testset', getDir('trainset', 'resized') + str(maxComponents) + 'PCABase.npy', maxComponents)


### QUERY :
def search_32x32():
	Timer.start('search_32x32')
	testDescriptorsFileName = getDir('testset', 'resized') + 'descriptors32x32.npy'
	trainDescriptorsFileName = getDir('trainset', 'resized') + 'descriptors32x32.npy'
	fileNamesFileName = getDir('trainset', 'resized') + 'fileNames.npy'
	resultMatchesFileName = getDir('results') + 'matches_' + '32x32.npy'
	matches = []

	for i in range(1, 101):
		testFileName = str(i) + '.jpg'

		testDescriptor = getDescriptor('testset', testDescriptorsFileName, testFileName)
		minValue, minIndex = calculateSSD('trainset', trainDescriptorsFileName, testDescriptor)
		fileNames = np.load(fileNamesFileName)
		resultFileName = fileNames[minIndex]
		print testFileName + ' -> ' + resultFileName
		matches.append({
			'test':  testFileName,
			'train': resultFileName
		})
	np.save(resultMatchesFileName, matches)
	Timer.stop('search_32x32')


def search_PCA(maxComponents):
	Timer.start('search_PCA' + str(maxComponents))
	testDescriptorsFileName = getDir('testset', 'resized') + str(maxComponents) + 'descriptorsPCA.npy'
	trainDescriptorsFileName = getDir('trainset', 'resized') + str(maxComponents) + 'descriptorsPCA.npy'
	fileNamesFileName = getDir('trainset', 'resized') + 'fileNames.npy'
	resultMatchesFileName = getDir('results') + 'matches_' + str(maxComponents) + 'PCA.npy'
	matches = []

	for i in range(1, 101):
		testFileName = str(i) + '.jpg'
		testDescriptor = getDescriptor('testset', testDescriptorsFileName, testFileName)
		minValue, minIndex = calculateSSD('trainset', trainDescriptorsFileName, testDescriptor)
		fileNames = np.load(fileNamesFileName)
		resultFileName = fileNames[minIndex]
		print testFileName + ' -> ' + resultFileName
		matches.append({
			'test':  testFileName,
			'train': resultFileName
		})

	np.save(resultMatchesFileName, matches)
	Timer.stop('search_PCA' + str(maxComponents))


def copyColorBetweenMatches(matchesFileName):
	matches = np.load(getDir('results') + matchesFileName)
	for match in matches:
		testFileName = match['test']
		trainFileName = match['train']
		print testFileName, trainFileName

		copyColorBetweenImages(
			getDir('trainset') + trainFileName,
			getDir('testset') + testFileName,
			getDir('results') + testFileName + '_COLOR-' + matchesFileName + '_' + trainFileName
		)
		copyImage(
			getDir('trainset') + trainFileName,
			getDir('results') + testFileName + '_copy-' + matchesFileName + '_' + trainFileName
		)


def copyColorBetweenMatches32():
	matchesFileName = 'matches_' + '32x32.npy'
	copyColorBetweenMatches(matchesFileName)


def copyColorBetweenMatchesPCA(maxComponents):
	matchesFileName = 'matches_' + str(maxComponents) + 'PCA.npy'
	copyColorBetweenMatches(matchesFileName)


def main():
	# maxComponents = 1024

	# prepare_resized()
	# prepare_descriptors32()
	# prepare_descriptorsPCA(19)
	# prepare_descriptorsPCA(1024)

	# search_32x32()
	# search_PCA(19)
	# search_PCA(1024)

	copyColorBetweenMatches32()
	copyColorBetweenMatchesPCA(19)
	copyColorBetweenMatchesPCA(1024)

	pass


Timer.start('program')
main()
Timer.stop('program')