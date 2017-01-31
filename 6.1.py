import cv2
import numpy as np
import scipy.io
from LabFiles import *
from lib.LightField import *
from lib.utils.Timer import *

def deconvL2_frequency(I, filt1, we):
	Timer.start('deconvL2_frequency')
	# note: size(filt1) is expected to be odd in both dimensions
	print I.shape
	print filt1.shape

	colorOriginalI = I.copy()
	I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)

	n, m = I.shape

	filt1 = np.fliplr(np.flipud(filt1))

	# compute prior
	Gx = np.fft.fft2(np.array([[-1, 1]]), (n, m))
	Gy = np.fft.fft2(np.array([[-1], [1]]), (n, m))

	# image after fft:
	F = np.fft.fft2(filt1, (n, m))

	# deconvolution:
	A = np.conj(F) * F + \
	    we * (np.conj(Gx) * Gx + np.conj(Gy) * Gy)
	b = np.conj(F) * np.fft.fft2(I)

	X = b / A

	# inverse fft:
	x = np.fft.ifft2(X)

	hs1 = int(np.floor((filt1.shape[0] - 1) / 2))
	hs2 = int(np.floor((filt1.shape[1] - 1) / 2))

	print hs1, hs2  # spike

	# get real part only
	xReal = x.real.clip(0, 255).astype(np.uint8)


	xColored = transferColor(colorOriginalI,xReal)
	# clipping edges:
	result = xColored[hs1:-hs1, hs2:-hs2]

	Timer.stop('deconvL2_frequency')
	return result


def readKernels():
	kernels = []
	for i in range(1, 10):
		filename = LabFiles.input(6, 1, 'filts-prefix') + str(i) + ".mat"
		fileValue = scipy.io.loadmat(filename)
		# print fileValue #spike
		kernel = fileValue['filts'][0, 3]
		kernels.append(kernel)
	return kernels

def transferColor(colorIm, grayIm):
	# print grayIm.shape
	colorIm = cv2.cvtColor(colorIm,cv2.COLOR_BGR2YCR_CB)
	colorIm[:,:,0] = grayIm
	result = cv2.cvtColor(colorIm, cv2.COLOR_YCR_CB2BGR)
	return result

def main():
	kernels = readKernels()
	imageClock = cv2.imread(LabFiles.input(6, 1, 'cups'))
	cv2.imwrite(LabFiles.output(6, 1, 'cups-original'), imageClock)

	results = []
	for index, kernel in enumerate(kernels):
		print 'deconvolution for kernel ' + str(index)
		result = deconvL2_frequency(imageClock, kernel, 0.01)

		# print result
		# break #spike
		cv2.imwrite(LabFiles.output(6, 1, 'cups-kernel-' + str(index + 1)), result)
		results.append(result)

	LabFiles.show(6, 1, 'cups-kernel-1')

main()