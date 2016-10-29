import cv2
import numpy as np
from LabFiles import *
from lib.utils.Timer import *
from lib.FocalStack import *

Timer.start('program')

# read file
im1 = cv2.imread(LabFiles.input(2, 1, 'stack-1'))
im2 = cv2.imread(LabFiles.input(2, 1, 'stack-2'))
im3 = cv2.imread(LabFiles.input(2, 1, 'stack-3'))

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

a = np.array([[1, 1],
              [1, 2]])

b = np.array([[2, 2],
              [2, 2]])


focalStack = FocalStack([a, b])
res = focalStack.calculateGradients()
print res
print res[:,:,0] #maxes
print res[:,:,1] #indexes maxes

# stoper
Timer.stop('program')

# show
#LabFiles.show(1, 5, 'raw-colors')