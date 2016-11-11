import cv2
from LabFiles import *
from lib.utils.Timer import *
from lib.Homography import *
from lib.HomographyFinder import *

Timer.start('program')


stata1 = cv2.imread(LabFiles.input(3, 4, 'stata-1'))
stata2 = cv2.imread(LabFiles.input(3, 4, 'stata-2'))


pointsStata1 = [[209, 218, 1], [425, 300, 1], [209, 337, 1], [396, 336, 1]]
pointsStata2 = [[232, 4, 1], [465, 62, 1], [247, 125, 1], [433, 102, 1]]

###
# stata-1 -> stata-2
homographyFinder = HomographyFinder(pointsStata1, pointsStata2)
calculatedHomography = homographyFinder.solve()
homography = Homography(calculatedHomography)

newShape, offset = homography.getNewShapeAndOffset(stata1, stata2)
print newShape, offset

result = homography.applyInterpolated(stata1, stata2, newShape, offset)
cv2.imwrite(LabFiles.output(3, 4, 'homographied-stata-1-2'), result)


# stoper
Timer.stop('program')

# show
LabFiles.show(3, 4, 'homographied-stata-1-2')