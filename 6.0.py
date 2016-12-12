import numpy as np
import cv2
import scipy.io

from LabFiles import *


def flip(kernel):
	kernelFlippedUpDown = np.flipud(kernel)
	kernelFlippedUpDownLeftRight = np.fliplr(kernelFlippedUpDown)
	return kernelFlippedUpDownLeftRight


def getKernelFromFiltObject(filtObject):
	result = filtObject['filts'][0, 3]
	return result


def getKernels():
	filtsFilenames = [LabFiles.input(6, 1, 'filts-prefix') + str(i) + ".mat" for i in range(1, 10)]
	filtsObjects = [scipy.io.loadmat(filename) for filename in filtsFilenames]
	result = [flip(getKernelFromFiltObject(filtObject)) for filtObject in filtsObjects]
	return result


def showKernels(kernelsImages):
	for kernelImage in kernelsImages:
		cv2.imshow('kernel', kernelImage)
		cv2.waitKey(0)


def kernel2Image(kernel):
	min, max = np.min(kernel), np.max(kernel)
	kernel = 255 * (kernel + min) / (max + min)  # (kernel - min) / (max-min) * 255 #spike-arczi:
	result = np.zeros((kernel.shape[0], kernel.shape[1], 3))
	result[..., 0] = kernel
	result[..., 1] = kernel
	result[..., 2] = kernel
	return result


def deconvolution_L2_frequency(I, F, Gx, Gy, weight):
	A = np.conj(F) * F + weight * (np.conj(Gx) * Gx + np.conj(Gy) * Gy)
	b = np.conj(F) * I
	X = b / A

	if len(I.shape) == 3:
		x = np.fft.ifft2(X, axes=(-3, -2))
	elif len(I.shape) == 2:
		x = np.fft.ifft2(X)
	else:
		raise NotImplementedError("Implemented for image with shape (h,w,c) or (h,w)")
	return x.real.clip(0, 255).astype(np.uint8)


def deconvL2_frequency():
	#("Making border for filtering...")
	max_fh = max(kernels, key=lambda x: x.shape[0]).shape[0]
	max_fw = max(kernels, key=lambda x: x.shape[1]).shape[1]
	(hfh, hfw) = (max_fh - 1) / 2, (max_fw - 1) / 2
	img_bord = cv2.copyMakeBorder(image, hfh, hfh, hfw, hfw, cv2.BORDER_REFLECT_101)

	#("Initializing data in frequency domain...")

	if len(img_bord.shape) == 3:
		image_fd = np.fft.fft2(img_bord, axes=(-3, -2))
		(n, m, c) = img_bord.shape
		kernels_fd = np.array([np.fft.fft2(k, (n, m)) for k in kernels])
		kernels_fd = np.repeat(kernels_fd[..., None], 3, axis=-1)
	elif len(img_bord.shape) == 2:
		image_fd = np.fft.fft2(img_bord)
		(n, m) = img_bord.shape
		kernels_fd = np.array([np.fft.fft2(k, (n, m)) for k in kernels])
	else:
		raise NotImplementedError("Implemented for image with shape (h,w,c) or (h,w)")

	#("Computing Gaussian Prior in frequency domain...")
	Gx, Gy = compute_prior_L2_frequency(image_fd)

	#("Computing deconvolution in frequency domain...")
	outputs = deconvolution_L2_frequency(image_fd, kernels_fd, Gx, Gy, 0.01)

	#("Aligning outputs...")
	for i in range(len(kernels)):
		fh, fw = kernels[i].shape[0], kernels[i].shape[1]
		hfh, hfw = fh / 2, fw / 2
		outputs[i, hfh:, hfw:] = outputs[i, :-hfh:, :-hfw]
	max_hfh, max_hfw = (outputs.shape[1] - image.shape[0]) / 2, (outputs.shape[2] - image.shape[1]) / 2
	outputs = outputs[:, max_hfh:-max_hfh, max_hfw:-max_hfw]
	return outputs

# GET INPUTS:
imageGray = cv2.imread(LabFiles.input(6, 1, 'clock'), 0)  # read image as grayscale

#GET KERNELS:
kernels = getKernels()
#spike:
# kernelsImages = [kernel2Image(kernel) for kernel in kernels]
# showKernels(kernelsImages)

# DECONVOLVE:




# outputs = deconvolution_L2(image, kernels)

# Input 3
# for i in range(len(kernels)):
# 	cv2.imwrite(LabFiles.output(6, 1, 'color_' + str(max(kernels[i].shape))), outputs[i])

# spike-removed: error in display_cups_board_color_output
# disp_path = LabFiles.output(6, 1, 'crop_color')
# display_cups_board_color_output(image, outputs, kernels, disp_path)
# cv2.imshow('crop_color', image)

# Input 4
# outputs_gray = deconvolution_L2(image_gray, kernels)
#
# outputs_colorized = []
# for i in range(len(kernels)):
# 	cv2.imwrite(LabFiles.output(6, 1, 'gray_' + str(max(kernels[i].shape))), outputs_gray[i])
# 	outputs_colorized.append(transfer_color(image, outputs_gray[i]))
# 	cv2.imwrite(LabFiles.output(6, 1, 'colorized_' + str(max(kernels[i].shape))), outputs_colorized[i])

# spike - removed: error in display_cups_board_color_output
# disp_path = LabFiles.output(6, 1, 'crop_colorized')
# display_cups_board_color_output(image, np.array(outputs_colorized), kernels, disp_path)
# cv2.imshow('crop_colorized', image)