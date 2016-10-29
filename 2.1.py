import cv2
import numpy as np
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
# test
# az = np.array([[[1, 0],
#                [1, 0]],
#
#               [[1, 0],
#                [2, 0]]])
# bz = np.array([[[2, 1],
#         [2, 1]],
#
#        [[2, 1],
#         [2, 1]]])
#
# a = np.array([[1, 1],
#               [1, 2]])
#
# b = np.array([[2, 2],
#               [2, 2]])
# focalStack = FocalStack([a, b])

focalStack = FocalStack([im1, im2, im3])
focalStack.run()
res = focalStack.getOutput()
cv2.imwrite(LabFiles.output(2, 1, 'focal-stacked'), res)
contributions = focalStack.getContributions()
for i in range(len(contributions)):
	#print i
	cv2.imwrite(LabFiles.output(2, 1, 'contribution-' + str(i)), contributions[i])


#spike-test ontributuins:
imTest = cv2.imread(LabFiles.output(2, 1, 'contribution-0'), cv2.IMREAD_GRAYSCALE)
print imTest

# print res
# print res[:,:,0] #maxes
# print res[:,:,1] #indexes maxes

# stoper
Timer.stop('program')

# show
LabFiles.show(2, 1, 'focal-stacked')