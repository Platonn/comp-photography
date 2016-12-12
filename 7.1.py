import cv2
import numpy as np
from LabFiles import *
from lib.LightField import *

images = LightField.readLightField('matrioska', number=9)
apretureView = LightField.getApertureView(images, borderWidth=0)
cv2.imwrite(LabFiles.output(7, 1, 'matrioska-apretureView', '.jpg'), apretureView)
