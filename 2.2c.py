import cv2
from LabFiles import *
from lib.utils.Timer import *
from lib.SimpleRobertson import *
from lib.utils.Normalizer import *
from lib.BilateralFilterToneMapper import *
from lib.SRGBCorrector import *

Timer.start('program')

# read file
images = [
	cv2.imread(LabFiles.input(2, 2, 'memorial-1'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH),
	cv2.imread(LabFiles.input(2, 2, 'memorial-2'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH),
	cv2.imread(LabFiles.input(2, 2, 'memorial-3'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH),
	cv2.imread(LabFiles.input(2, 2, 'memorial-4'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH),
	cv2.imread(LabFiles.input(2, 2, 'memorial-5'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH),
	cv2.imread(LabFiles.input(2, 2, 'memorial-6'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH),
	cv2.imread(LabFiles.input(2, 2, 'memorial-7'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH),
	cv2.imread(LabFiles.input(2, 2, 'memorial-8'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH),
	cv2.imread(LabFiles.input(2, 2, 'memorial-9'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH),
	cv2.imread(LabFiles.input(2, 2, 'memorial-10'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH),
	cv2.imread(LabFiles.input(2, 2, 'memorial-11'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH),
	cv2.imread(LabFiles.input(2, 2, 'memorial-12'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH),
	cv2.imread(LabFiles.input(2, 2, 'memorial-13'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH),
	cv2.imread(LabFiles.input(2, 2, 'memorial-14'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH),
	cv2.imread(LabFiles.input(2, 2, 'memorial-15'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH),
	cv2.imread(LabFiles.input(2, 2, 'memorial-16'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH),
]

exposures = [
	LabFiles.exposureTime(2, 2, 'memorial-1'),
	LabFiles.exposureTime(2, 2, 'memorial-2'),
	LabFiles.exposureTime(2, 2, 'memorial-3'),
	LabFiles.exposureTime(2, 2, 'memorial-4'),
	LabFiles.exposureTime(2, 2, 'memorial-5'),
	LabFiles.exposureTime(2, 2, 'memorial-6'),
	LabFiles.exposureTime(2, 2, 'memorial-7'),
	LabFiles.exposureTime(2, 2, 'memorial-8'),
	LabFiles.exposureTime(2, 2, 'memorial-9'),
	LabFiles.exposureTime(2, 2, 'memorial-10'),
	LabFiles.exposureTime(2, 2, 'memorial-11'),
	LabFiles.exposureTime(2, 2, 'memorial-12'),
	LabFiles.exposureTime(2, 2, 'memorial-13'),
	LabFiles.exposureTime(2, 2, 'memorial-14'),
	LabFiles.exposureTime(2, 2, 'memorial-15'),
	LabFiles.exposureTime(2, 2, 'memorial-16'),
]

# normalize images
images = [Normalizer.from8bit(image) for image in images]
# linearize from sRGB
linear_images = [SRGBCorrector.apply_inversed_sRGB(image) for image in images]

# zip - 2 versions (without linearize and with)
imagesWithExposures = zip(images, exposures)
linear_imagesWithExposures = zip(linear_images, exposures)

# process - version without linearization
result = SimpleRobertson.merge(imagesWithExposures)
cv2.imwrite(LabFiles.output(2, 2, 'memorial-fromSRGB', '.exr'), result)
resultToneMapped = BilateralFilterToneMapper.run(result, -1, 0.4, 5, 30)
cv2.imwrite(LabFiles.output(2, 2, 'memorial-fromSRGB-toneMapped'), resultToneMapped)

# process - version with linearization
linear_result = SimpleRobertson.merge(linear_imagesWithExposures)
cv2.imwrite(LabFiles.output(2, 2, 'memorial-linearized-fromSRGB', '.exr'), linear_result)
linear_resultToneMapped = BilateralFilterToneMapper.run(linear_result, -1, 0.4, 5, 30)
cv2.imwrite(LabFiles.output(2, 2, 'memorial-linearized-fromSRGB-toneMapped'), linear_resultToneMapped)

# stoper
Timer.stop('program')

# show
# LabFiles.show(2, 2, 'sec3-hdr-fromSRGB', '.exr')
LabFiles.show(2, 2, 'memorial-linearized-fromSRGB-toneMapped')