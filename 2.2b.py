import cv2
from LabFiles import *
from lib.utils.Timer import *
from lib.SimpleRobertson import *
from lib.utils.Normalizer import *
from lib.BilateralFilterToneMapper import *
from lib.SRGBCorrector import *

Timer.start('program')

# read file
imSec3_1 = cv2.imread(LabFiles.input(2, 2, 'sec3-1-16bit-srgb'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
imSec3_1_exposure = LabFiles.exposureTime(2, 2, 'sec3-1')

imSec3_2 = cv2.imread(LabFiles.input(2, 2, 'sec3-2-16bit-srgb'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
imSec3_2_exposure = LabFiles.exposureTime(2, 2, 'sec3-2')

imSec3_3 = cv2.imread(LabFiles.input(2, 2, 'sec3-3-16bit-srgb'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
imSec3_3_exposure = LabFiles.exposureTime(2, 2, 'sec3-3')

imSec3_1 = Normalizer.from16bit(imSec3_1)
imSec3_2 = Normalizer.from16bit(imSec3_2)
imSec3_3 = Normalizer.from16bit(imSec3_3)

# for comparsion - without linearization:
# # process
# imagesWithExposures = [
# 	(imSec3_1, imSec3_1_exposure),
# 	(imSec3_2, imSec3_2_exposure),
# 	(imSec3_3, imSec3_3_exposure)
# ]
# result = SimpleRobertson.merge(imagesWithExposures)
# cv2.imwrite(LabFiles.output(2, 2, 'sec3-hdr-fromSRGB', '.exr'), result)
# resultToneMapped = BilateralFilterToneMapper.run(result, -1, 0.4, 10, 12)
# cv2.imwrite(LabFiles.output(2, 2, 'sec3-hdr-fromSRGB-toneMapped'), resultToneMapped)

# LINEARIZE AND REPEAT:
linear_imSec3_1 = SRGBCorrector.apply_inversed_sRGB(imSec3_1)
linear_imSec3_2 = SRGBCorrector.apply_inversed_sRGB(imSec3_2)
linear_imSec3_3 = SRGBCorrector.apply_inversed_sRGB(imSec3_3)

linear_imagesWithExposures = [
	(linear_imSec3_1, imSec3_1_exposure),
	(linear_imSec3_2, imSec3_2_exposure),
	(linear_imSec3_3, imSec3_3_exposure)
]
linear_result = SimpleRobertson.merge(linear_imagesWithExposures)
cv2.imwrite(LabFiles.output(2, 2, 'sec3-hdr-linearized-fromSRGB', '.exr'), linear_result)
linear_resultToneMapped = BilateralFilterToneMapper.run(linear_result, -1, 0.3, 10, 30)
cv2.imwrite(LabFiles.output(2, 2, 'sec3-hdr-linearized-fromSRGB-toneMapped'), linear_resultToneMapped )


# stoper
Timer.stop('program')

# show
# LabFiles.show(2, 2, 'sec3-hdr-fromSRGB', '.exr')
LabFiles.show(2, 2, 'sec3-hdr-linearized-fromSRGB-toneMapped')