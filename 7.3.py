import cv2
import numpy as np
from LabFiles import *
from lib.utils.Normalizer import *
from lib.LightField import *

def getDisplacementVideo(name, number):
	images = LightField.readLightField(name, number)
	images = LightField.normalizeImages(images)

	steps = np.arange(-1.5, 2.1, 0.1)
	LightField.displacementVideo(LabFiles.output(7, 3, name + '-displacement', '.avi'), images, steps)
	LabFiles.show(7, 3, name + '-displacement', '.avi')

getDisplacementVideo('matrioska', 9)
# getDisplacementVideo('motorbike', 9)
# getDisplacementVideo('building', 17)
