import cv2
from LabFiles import *
from lib.utils.Timer import *
from lib.Homography import *
from lib.HomographyFinder import *

Timer.start('program')

# read file
# imGreen = cv2.imread(LabFiles.input(3, 3, 'green'))
# imPoster = cv2.imread(LabFiles.input(3, 3, 'poster'))

# print result

# cv2.imwrite(LabFiles.output(3, 2, 'homographied-interpolated'), result)
# cv2.imwrite(LabFiles.output(3, 2, 'homographied-interpolated'), result)

#spike:
points1 = np.array([
	[1., 2., 1.], [3., 4., 1.], [5., 6., 1.], [7., 8., 1.]
])
points2 = np.array([
	[-1., -2., -1.], [-3., -4., -1.], [-5., -6., -1.], [-7., -8., -1.]
])
homographyFinder = HomographyFinder(points1, points2)
homographyFinder.solve()

# stoper
Timer.stop('program')

# show
# LabFiles.show(3, 2, 'homographied-interpolated')