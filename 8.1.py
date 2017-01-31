import cv2
import numpy as np
import scipy.io
from LabFiles import *
from lib.LightField import *
from lib.utils.Timer import *


def naivePaste(maskIm, objectIm, backgroundIm, objectPasteLopLeft):
	y, x = objectPasteLopLeft
	height, width, _ = objectIm.shape

	# spike-new:
	mask = (maskIm / 255.0)
	invMask = 1.0 - mask
	# cv2.imshow('', invMask) #spike
	# cv2.waitKey(0)

	objectImMasked = objectIm * mask

	# cv2.imshow('', objectImMasked) #spike
	# cv2.waitKey(0)

	result = backgroundIm.copy()
	result[y:y + height, x:x + width] *= invMask
	result[y:y + height, x:x + width] += objectImMasked
	return result


def main():
	maskIm = cv2.imread(LabFiles.input(8, 1, 'mask')).astype(np.float32)
	objectIm = cv2.imread(LabFiles.input(8, 1, 'object')).astype(np.float32)
	backgroundIm = cv2.imread(LabFiles.input(8, 1, 'background')).astype(np.float32)

	result = naivePaste(maskIm, objectIm, backgroundIm, (0, 0))
	cv2.imwrite(LabFiles.output(8, 1, 'naive-paste'), result)
	LabFiles.show(8, 1, 'naive-paste')


main()