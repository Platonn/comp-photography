import numpy as np
import cv2
import scipy.io

from LabFiles import *


# display helper:
def multiple_display(array):
	sizes = []
	disp_shape = list(array[0][0].shape)
	disp_shape[0] = disp_shape[1] = 0
	for y in range(0, len(array)):
		width = 0
		height = 0
		for x in range(0, len(array[y])):
			width += array[y][x].shape[1]
			height = max(height, array[y][x].shape[0])
		sizes.append([height, width])
		disp_shape[1] = max(disp_shape[1], width)
		disp_shape[0] = disp_shape[0] + height

	output_display = np.zeros(tuple(disp_shape), array[0][0].dtype)

	row_pos = 0
	for y in range(0, len(array)):
		col_pos = 0
		for x in range(0, len(array[y])):
			h, w = array[y][x].shape[0], array[y][x].shape[1]
			output_display[row_pos:row_pos + h, col_pos:col_pos + w] = array[y][x]
			col_pos += w
		row_pos += sizes[y][0]

	return output_display


def draw_point(img, A):
	cv2.rectangle(img, (A[0] - 1, A[1] - 1), (A[0] + 1, A[1] + 1), (0, 255, 0), -1)


def draw_arrow(img, A, B):
	cv2.line(img, A, B, (255, 0, 0), 1, 8)
	cv2.rectangle(img, (A[0] - 1, A[1] - 1), (A[0] + 1, A[1] + 1), (0, 255, 0), -1)
	cv2.rectangle(img, (B[0] - 1, B[1] - 1), (B[0] + 1, B[1] + 1), (0, 0, 255), -1)


def draw_circle_on_center(img):
	(h, w, c) = img.shape
	center = (w / 2, h / 2)
	radius = min(w / 2, h / 2)
	cv2.circle(img, center, radius, (255, 255, 255))


def draw_rectangle_on_center(img):
	(h, w, c) = img.shape
	center = (w / 2, h / 2)
	rw = w
	rh = w / 2
	cv2.rectangle(img, (0, h / 2 - rh / 2), (w - 1, h / 2 + rh / 2), (255, 255, 255))


def normalized_copy(img):
	return img * (255. / np.max(img))


def display_cups_board_color_output(image, outputs, kernels, path):
	crop_area1 = np.array([[250, 400], [650, 800]])
	crop_area2 = np.array([[850, 1000], [850, 1000]])
	outputs_crop1 = outputs[:, crop_area1[0, 0]:crop_area1[0, 1], crop_area1[1, 0]:crop_area1[1, 1]].copy()
	outputs_crop2 = outputs[:, crop_area2[0, 0]:crop_area2[0, 1], crop_area2[1, 0]:crop_area2[1, 1]].copy()

	outdisp1 = []
	outdisp2 = []
	for i in range(len(kernels)):
		k = kernels[i]
		kernel_disp = (k + np.min(k)) * (255. / (np.max(k) + np.min(k)))
		kernel_disp = np.repeat(kernel_disp[..., None], 3, axis=-1)
		out_img1 = outputs_crop1[i]
		out_img2 = outputs_crop2[i]

		print out_img1.shape, k.shape, kernel_disp.shape  # spike
		out_img1[:k.shape[0], :k.shape[1]] = kernel_disp
		out_img2[:k.shape[0], :k.shape[1]] = kernel_disp
		outdisp1.append(out_img1)
		outdisp2.append(out_img2)

	img_crop1 = image[crop_area1[0, 0]:crop_area1[0, 1], crop_area1[1, 0]:crop_area1[1, 1]].copy()
	img_crop2 = image[crop_area2[0, 0]:crop_area2[0, 1], crop_area2[1, 0]:crop_area2[1, 1]].copy()
	outdisp1.append(img_crop1)
	outdisp2.append(img_crop2)

	outdisp = outdisp1 + outdisp2

	outdisp = [outdisp[i * 5:i * 5 + 5] for i in range(int(np.ceil(len(outdisp) / 5.)))]

	output_crop_display = multiple_display(outdisp)
	cv2.imwrite(path, output_crop_display)


# Transfer colors:
def transfer_color(img_src, img_dest):
	if len(img_dest.shape) == 2:
		(h, w) = img_dest.shape
		img_dest_valid = np.repeat(img_dest[..., None], 3, axis=-1)
	elif len(img_dest.shape) == 3:
		(h, w, c) = img_dest.shape
		img_dest_valid = img_dest.copy()
	else:
		raise NotImplementedError("Implemented for img_dest with shape (h,w,c) or (h,w)")
	if (img_src.shape[:2] != img_dest.shape[:2]):
		img_src_valid = cv2.resize(img_src, (w, h))
	else:
		img_src_valid = img_src
	img_src_YCrCb = cv2.cvtColor(img_src_valid, cv2.COLOR_BGR2YCR_CB)
	out_YCrCb = cv2.cvtColor(img_dest_valid, cv2.COLOR_BGR2YCR_CB)
	out_YCrCb[:, :, 1] = img_src_YCrCb[:, :, 1]
	out_YCrCb[:, :, 2] = img_src_YCrCb[:, :, 2]
	out_BGR = cv2.cvtColor(out_YCrCb, cv2.COLOR_YCR_CB2BGR)
	return out_BGR


# Input 1:
def compute_prior_L2_frequency(I):
	if len(I.shape) == 3:
		(n, m, c) = I.shape
	elif len(I.shape) == 2:
		(n, m) = I.shape
	else:
		raise NotImplementedError("Implemented for image with shape (h,w,c) or (h,w)")
	Gx = np.fft.fft2(np.array([[-1, 1]]), (n, m))
	Gy = np.fft.fft2(np.array([[-1], [1]]), (n, m))
	if len(I.shape) == 3:
		Gx = np.repeat(Gx[..., None], c, axis=-1)
		Gy = np.repeat(Gy[..., None], c, axis=-1)
	return Gx, Gy


# kernel size is expected to be odd in both dimensions
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


def flip_kernel(kernel):
	return np.fliplr(np.flipud(kernel))


def deconvolution_L2(image, kernels):
	print ("Making border for filtering...")
	max_fh = max(kernels, key=lambda x: x.shape[0]).shape[0]
	max_fw = max(kernels, key=lambda x: x.shape[1]).shape[1]
	(hfh, hfw) = (max_fh - 1) / 2, (max_fw - 1) / 2
	img_bord = cv2.copyMakeBorder(image, hfh, hfh, hfw, hfw, cv2.BORDER_REFLECT_101)

	print ("Initializing data in frequency domain...")

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

	print ("Computing Gaussian Prior in frequency domain...")
	Gx, Gy = compute_prior_L2_frequency(image_fd)

	print ("Computing deconvolution in frequency domain...")
	outputs = deconvolution_L2_frequency(image_fd, kernels_fd, Gx, Gy, 0.01)

	print ("Aligning outputs...")
	for i in range(len(kernels)):
		fh, fw = kernels[i].shape[0], kernels[i].shape[1]
		hfh, hfw = fh / 2, fw / 2
		outputs[i, hfh:, hfw:] = outputs[i, :-hfh:, :-hfw]
	max_hfh, max_hfw = (outputs.shape[1] - image.shape[0]) / 2, (outputs.shape[2] - image.shape[1]) / 2
	outputs = outputs[:, max_hfh:-max_hfh, max_hfw:-max_hfw]
	return outputs


# Input 2
matlabFilenames = [LabFiles.input(6, 1, 'filts-prefix') + str(i) + ".mat" for i in range(1, 10)]
print matlabFilenames  # spike
matlab_files = [scipy.io.loadmat(filename) for filename in matlabFilenames]

print matlab_files[0]

kernels = [flip_kernel(ml_file['filts'][0, 3]) for ml_file in matlab_files]
image = cv2.imread(LabFiles.input(6, 1, 'clock'))
image_gray = cv2.imread(LabFiles.input(6, 1, 'clock'), 0)

outputs = deconvolution_L2(image, kernels)

# Input 3
for i in range(len(kernels)):
	cv2.imwrite(LabFiles.output(6, 1, 'color_' + str(max(kernels[i].shape))), outputs[i])

#spike-removed: error in display_cups_board_color_output
# disp_path = LabFiles.output(6, 1, 'crop_color')
# display_cups_board_color_output(image, outputs, kernels, disp_path)
# cv2.imshow('crop_color', image)

# Input 4
outputs_gray = deconvolution_L2(image_gray, kernels)

outputs_colorized = []
for i in range(len(kernels)):
	cv2.imwrite(LabFiles.output(6, 1, 'gray_' + str(max(kernels[i].shape))), outputs_gray[i])
	outputs_colorized.append(transfer_color(image, outputs_gray[i]))
	cv2.imwrite(LabFiles.output(6, 1, 'colorized_' + str(max(kernels[i].shape))), outputs_colorized[i])

#spike - removed: error in display_cups_board_color_output
# disp_path = LabFiles.output(6, 1, 'crop_colorized')
# display_cups_board_color_output(image, np.array(outputs_colorized), kernels, disp_path)
# cv2.imshow('crop_colorized', image)