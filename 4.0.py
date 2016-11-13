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
		print 'ERROR - images shapes dont match'
		cv2.imwrite(outputFileName, grayIm)
	else:
		colorIm = cv2.cvtColor(colorIm, cv2.COLOR_BGR2YCR_CB)
		grayIm = cv2.cvtColor(grayIm, cv2.COLOR_BGR2YCR_CB)
		grayIm[:, :, 1:] = colorIm[:, :, 1:]  # copy CrCb channels
		grayIm = cv2.cvtColor(grayIm, cv2.COLOR_YCR_CB2BGR)
		cv2.imwrite(outputFileName, grayIm)


def main():
	maxComponents = 19

	# preparation code:
	# filesResizeTo32('test')
	# filesResizeTo32('train')
	# filesGet32x32Descriptor('test')
	# filesGet32x32Descriptor('train')

	### spike:
	### calculatePCABase('test')

	# calculatePCABase('train', maxComponents)
	# getPCADescriptors('train', getDir('train', 'resized') + str(maxComponents) + 'PCABase.npy', maxComponents)
	# getPCADescriptors('test', getDir('train', 'resized') + str(maxComponents) + 'PCABase.npy', maxComponents)

	# query code:

	# 32x32:
	# Timer.start('search 32x32')
	# for i in range(1, 101):
	# 	testFileName = str(i) + '.jpg'
	# 	testDescriptor = getDescriptor('test', getDir('test', 'resized') + 'descriptors32x32.npy',
	# 	                               testFileName)  # descriptorsPCA.npy
	# 	minValue, minIndex = calculateSSD('train', getDir('train', 'resized') + 'descriptors32x32.npy',
	# 	                                  testDescriptor)  # descriptorsPCA.npy #train
	# 	fileNames = np.load(getDir('train', 'resized') + 'fileNames.npy')
	# 	resultFileName = fileNames[minIndex]
	# 	print testFileName + ' -> ' + resultFileName
	# 	# os.system('cp ' + getDir('train') + resultFileName + ' ../4/in/results/' + testFileName + '_32x32_' + resultFileName)
	# 	copyColorBetweenImages(getDir('train') + resultFileName,
	# 	                       getDir('test') + testFileName,
	# 	                       '../4/in/results/' + testFileName + '_32x32_' + 'COLOR' + resultFileName)
	# Timer.stop('search 32x32')

	# PCA
	Timer.start('search PCA' + str(maxComponents))
	for i in range(1, 101):
		testFileName = str(i) + '.jpg'
		testDescriptor = getDescriptor('test', getDir('test', 'resized') + str(maxComponents) + 'descriptorsPCA.npy',
		                               testFileName)  # descriptorsPCA.npy
		minValue, minIndex = calculateSSD('train', getDir('train', 'resized') + str(maxComponents) + 'descriptorsPCA.npy',
		                                  testDescriptor)  # descriptorsPCA.npy #train
		fileNames = np.load(getDir('train', 'resized') + 'fileNames.npy')
		resultFileName = fileNames[minIndex]
		print testFileName + ' -> ' + resultFileName
		# os.system('cp ' + getDir('train') + resultFileName + ' ../4/in/results/' + testFileName + '-' + str(maxComponents) + 'PCA-' + resultFileName)
		copyColorBetweenImages(getDir('train') + resultFileName,
		                       getDir('test') + testFileName,
		                       '../4/in/results/' + testFileName + '-' + str(
			                       maxComponents) + 'PCA-' + 'COLOR' + resultFileName)
	Timer.stop('search PCA' + str(maxComponents))

	# singular test:
	# testFileName = '78.jpg'
	# testDescriptor = getDescriptor('test', getDir('test', 'resized') + 'descriptorsPCA.npy', testFileName)
	# minValue, minIndex = calculateSSD('test', getDir('test', 'resized') + 'descriptorsPCA.npy', testDescriptor)
	# fileNames = np.load(getDir('test', 'resized') + 'fileNames.npy') #train
	# resultFileName = fileNames[minIndex]
	# print str(minValue)
	# print testFileName + ' -> ' + resultFileName
	pass


Timer.start('program')
main()
Timer.stop('program')