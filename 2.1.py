import cv2
from LabFiles import *
from lib.utils.Timer import *
from lib.FocalStack import *

Timer.start('program')

# read file
im1 = cv2.imread(LabFiles.input(2, 1, 'stack-1'), cv2.IMREAD_GRAYSCALE)
im2 = cv2.imread(LabFiles.input(2, 1, 'stack-2'), cv2.IMREAD_GRAYSCALE)
im3 = cv2.imread(LabFiles.input(2, 1, 'stack-3'), cv2.IMREAD_GRAYSCALE)

cv2.imwrite(LabFiles.output(2, 1, 'stack-1'), im1)
cv2.imwrite(LabFiles.output(2, 1, 'stack-2'), im2)
cv2.imwrite(LabFiles.output(2, 1, 'stack-3'), im3)

focalStack = FocalStack([im1, im2, im3])
focalStack.run()

res = focalStack.getOutput()
cv2.imwrite(LabFiles.output(2, 1, 'focal-stacked'), res)

contributions = focalStack.getContributions()
for i in range(len(contributions)):
	cv2.imwrite(LabFiles.output(2, 1, 'contribution-' + str(i)), contributions[i])

# stoper
Timer.stop('program')

# show
LabFiles.show(2, 1, 'focal-stacked')