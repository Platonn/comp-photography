import cv2
from LabFiles import *
from lib.utils.Timer import *
from lib.SimpleRobertson import *
from lib.utils.Normalizer import *
from lib.BilateralFilterToneMapper import  *
from lib.GammaCorrector import *





#SPIKE - TODO: Zaczac robic w tym pliku 2.2b !!! (poki co to jest kopia 2.2a)





Timer.start('program')

# read file
imSec3_1 = cv2.imread(LabFiles.input(2, 2, 'sec3-1-srgb'))
imSec3_1_exposure = LabFiles.exposureTime(2, 2, 'sec3-1')

imSec3_2 = cv2.imread(LabFiles.input(2, 2, 'sec3-2-srgb'))
imSec3_2_exposure = LabFiles.exposureTime(2, 2, 'sec3-2')

imSec3_3 = cv2.imread(LabFiles.input(2, 2, 'sec3-3-srgb'))
imSec3_3_exposure = LabFiles.exposureTime(2, 2, 'sec3-3')

#normalize tiff 16bit images
imSec3_1 = Normalizer.from16bit(imSec3_1)
imSec3_2 = Normalizer.from16bit(imSec3_2)
imSec3_3 = Normalizer.from16bit(imSec3_3)

#process
imagesWithExposures = [
	(imSec3_1, imSec3_1_exposure),
	(imSec3_2, imSec3_2_exposure),
	(imSec3_3, imSec3_3_exposure)
]
result = SimpleRobertson.merge(imagesWithExposures)

cv2.imwrite(LabFiles.output(2, 2, 'sec3-hdr', '.exr'), result)


print result
resultToneMapped = BilateralFilterToneMapper.run(result, -1, 0.3, 12, 10000)
print resultToneMapped
cv2.imwrite(LabFiles.output(2, 2, 'sec3-hdr-toneMapped'), resultToneMapped)


# stoper
Timer.stop('program')

# show
#LabFiles.show(2, 2, 'sec3-hdr', '.exr')
LabFiles.show(2, 2, 'sec3-hdr-toneMapped')
