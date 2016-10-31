import cv2
from LabFiles import *
from lib.utils.Timer import *
from lib.BilateralFilterToneMapper import *

Timer.start('program')

# read file
imExr = cv2.imread(LabFiles.input(2, 3, 'exr'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
#print imExr

result = BilateralFilterToneMapper.run(imExr)

cv2.imwrite(LabFiles.output(2, 3, 'tone-mapped'), result)

# stoper
Timer.stop('program')

# show
LabFiles.show(2, 3, 'tone-mapped')