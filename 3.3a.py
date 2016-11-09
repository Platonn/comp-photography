import cv2
from LabFiles import *
from lib.utils.Timer import *
from lib.Homography import *
from lib.HomographyFinder import *

Timer.start('program')

# green -> poster
imGreen = cv2.imread(LabFiles.input(3, 3, 'green'))
imPoster = cv2.imread(LabFiles.input(3, 3, 'poster'))

(h, w, _) = imPoster.shape
h, w = h - 1, w - 1
pointsPoster = np.array([[0, 0, 1], [0, w, 1], [h, w, 1], [h, 0, 1]])
pointsGreen = np.array([[170, 95, 1], [171, 238, 1], [233, 235, 1], [239, 94, 1]])

homographyFinder = HomographyFinder(pointsPoster, pointsGreen)
calculatedHomography = homographyFinder.solve()

homography = Homography(calculatedHomography)
result = homography.applyInterpolated(imPoster, imGreen)

cv2.imwrite(LabFiles.output(3, 3, 'homographied-green-poster'), result)

# stoper
Timer.stop('program')

# show
LabFiles.show(3, 3, 'homographied-green-poster')