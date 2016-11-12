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


# spike function
def countFiles(target):
	feedbackObject = {'counter': 0}

	def count(inFolder, fileName, feedbackObject):
		feedbackObject['counter'] += 1

	applyFunctionToFiles(count, 'count', getDir(target), '.jpg', feedbackObject)
	print "number of files: " + str(feedbackObject['counter'])


def calculateSSD(target, descriptorsFileName, testDescriptor):
	#Timer.start('calculateSSD')
	descriptors = np.load(descriptorsFileName)
	testDescriptorMatrix = np.zeros(descriptors.shape)
	testDescriptorMatrix[...] = testDescriptor

	def ssdPerRow(descriptorsRow, testDescriptor):
		return np.sum((descriptorsRow - testDescriptor) ** 2)

	ssdValues = np.apply_along_axis(ssdPerRow, 1, descriptors, testDescriptor)
	minSsdValue = np.min(ssdValues)
	minSsdValueIndex = np.argmin(ssdValues)
	#print minSsdValue
	#Timer.stop('calculateSSD')
	return (minSsdValue, minSsdValueIndex)


def calculatePCABase(target):
	Timer.start('calculatePCABase')

	Timer.start('calculatePCABase load descriptors32x32')
	descriptors32x32 = np.load(getDir(target, 'resized') + 'descriptors32x32.npy')
	Timer.stop('calculatePCABase load descriptors32x32')

	Timer.start('calculatePCABase PCACompute')
	PCABase = cv2.PCACompute(descriptors32x32, maxComponents=19)  # (meanPCA, eigenvectorsPCA)
	Timer.stop('calculatePCABase PCACompute')

	np.save(getDir(target, 'resized') + 'PCABase.npy', PCABase)
	Timer.stop('calculatePCABase')


def getPCADescriptors(target, PCABaseFileName):
	Timer.start('getPCADescriptors')
	PCABase = np.load(PCABaseFileName)
	meanPCA, eigenvectorsPCA = PCABase
	descriptors32x32 = np.load(getDir(target, 'resized') + 'descriptors32x32.npy')
	descriptorsPCA = cv2.PCAProject(descriptors32x32, meanPCA, eigenvectorsPCA)
	np.save(getDir(target, 'resized') + 'descriptorsPCA.npy', descriptorsPCA)
	Timer.stop('getPCADescriptors')


def getColorFromImage(inFolder, inFileName, outFolder, outFileName):
	# otworzyc obrazek IN i OUT
	# przekonwertowac IN i OUT na YCrCb
	# przekopiowac Cr i Cb ([1] i [2] kanaL) z IN do OUT
	# skonwertowac OUT do RGB, zapisac OUT
	pass


def getDescriptor(target, descriptorsFileName, fileName):
	fileNames = np.load(getDir(target, 'resized') + 'fileNames.npy')
	descriptors = np.load(descriptorsFileName)
	index = np.where(fileNames == fileName)
	descriptor = descriptors[index]
	result = descriptor[0]
	return result


def main():
	# preparation code:
	# filesResizeTo32('test')
	# filesResizeTo32('train')
	# filesGet32x32Descriptor('test')
	# filesGet32x32Descriptor('train')
	# calculatePCABase('test')
	# calculatePCABase('train')
	# getPCADescriptors('test', getDir('test', 'resized') + 'PCABase.npy')
	# getPCADescriptors('train', getDir('train', 'resized') + 'PCABase.npy')

	# query code:

	# 32x32:
	# for i in range(1,101):
	# 	testFileName = str(i) + '.jpg'
	# 	testDescriptor = getDescriptor('test', getDir('test', 'resized') + 'descriptors32x32.npy', testFileName) #descriptorsPCA.npy
	# 	minValue, minIndex = calculateSSD('train', getDir('train', 'resized') + 'descriptors32x32.npy', testDescriptor) #descriptorsPCA.npy #train
	# 	fileNames = np.load(getDir('train', 'resized') + 'fileNames.npy') #train
	# 	resultFileName = fileNames[minIndex]
	#
	# 	print testFileName + ' -> ' + resultFileName
	#
	# 	os.system('cp ' + getDir('train') + resultFileName + ' ../4/in/results/' + testFileName + '-32x32-' + resultFileName)

	# PCA
	# for i in range(1,101):
	# 	testFileName = str(i) + '.jpg'
	# 	testDescriptor = getDescriptor('test', getDir('test', 'resized') + 'descriptorsPCA.npy', testFileName) #descriptorsPCA.npy
	# 	minValue, minIndex = calculateSSD('train', getDir('train', 'resized') + 'descriptorsPCA.npy', testDescriptor) #descriptorsPCA.npy #train
	# 	fileNames = np.load(getDir('train', 'resized') + 'fileNames.npy') #train
	# 	resultFileName = fileNames[minIndex]
	#
	# 	print testFileName + ' -> ' + resultFileName
	#
	# 	os.system('cp ' + getDir('train') + resultFileName + ' ../4/in/results/' + testFileName + '-PCA-' + resultFileName)

	testFileName = '78.jpg'
	testDescriptor = getDescriptor('test', getDir('test', 'resized') + 'descriptorsPCA.npy', testFileName)
	minValue, minIndex = calculateSSD('test', getDir('test', 'resized') + 'descriptorsPCA.npy', testDescriptor)
	fileNames = np.load(getDir('test', 'resized') + 'fileNames.npy') #train
	resultFileName = fileNames[minIndex]
	print str(minValue)
	print testFileName + ' -> ' + resultFileName

	# testDescriptor = getDescriptor('test', getDir('test', 'resized') + 'descriptors32x32.npy', '1.jpg')
	# calculateSSD('test', getDir('test', 'resized') + 'descriptors32x32.npy', testDescriptor)



Timer.start('program')
main()
Timer.stop('program')