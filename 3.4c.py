import cv2
from LabFiles import *
from lib.utils.Timer import *
from lib.Homography import *
from lib.HomographyFinder import *

Timer.start('program')


sunset1 = cv2.imread(LabFiles.input(3, 4, 'sunset-1'))
sunset2 = cv2.imread(LabFiles.input(3, 4, 'sunset-2'))

pointsSunset1 = [[177, 258, 1], [180, 420, 1], [191, 421, 1], [195, 270, 1]]
pointsSunset2 = [[177, 97, 1], [183, 258, 1], [193, 258, 1], [195, 109, 1]]

###
# sunset-2 -> sunset-1
homographyFinder = HomographyFinder(pointsSunset2, pointsSunset1)
calculatedHomography = homographyFinder.solve()
homography = Homography(calculatedHomography)

newShape, offset = homography.getNewShapeAndOffset(sunset2, sunset1)
print newShape, offset
result = homography.applyInterpolated(sunset2, sunset1, newShape, offset)
cv2.imwrite(LabFiles.output(3, 4, 'homographied-sunset-2-1'), result)

# stoper
Timer.stop('program')

# show
LabFiles.show(3, 4, 'homographied-sunset-2-1')