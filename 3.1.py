import cv2
from LabFiles import *
from lib.utils.Timer import *
from lib.Homography import *

Timer.start('program')

# read file
imGreen = cv2.imread(LabFiles.input(3, 1, 'green'))
imPoster = cv2.imread(LabFiles.input(3, 1, 'poster'))

homography = Homography(np.array([[0.8346, -0.0058, -141.3292],
                                  [0.0116, 0.8025, -78.2148],
                                  [-0.0002, -0.0006, 1.]]))

result = homography.applyNeighbour(imPoster,imGreen)

# print result

cv2.imwrite(LabFiles.output(3, 1, 'homographied-neighbourFill'), result)

# stoper
Timer.stop('program')

# show
LabFiles.show(3, 1, 'homographied-neighbourFill')