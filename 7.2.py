import cv2
import numpy as np
from LabFiles import *
from lib.LightField import *

name = 'matrioska'
images = LightField.readLightField(name, number=9)
horizontalSlices = LightField.getHorizontalSlices(images)
verticalSlices = LightField.getVerticalSlices(images)
cv2.imwrite(LabFiles.output(7,2, name + '-horizontalSlices'), horizontalSlices)
cv2.imwrite(LabFiles.output(7,2, name + '-verticalSlices'), verticalSlices)
