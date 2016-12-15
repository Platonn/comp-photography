import cv2
import numpy as np
from LabFiles import *
from lib.utils.Normalizer import *
from lib.LightField import *

def getDisplacementVideo(name, number, aperture, steps):
	images = LightField.readLightField(name, number)
	images = LightField.normalizeImages(images)
	LightField.displacementVideo(LabFiles.output(7, 3, name + '-displacement', '.avi'), images, aperture, steps)
	LabFiles.show(7, 3, name + '-displacement', '.avi')

def getMovingApertureVideo(name, number, aperture, steps):
	images = LightField.readLightField(name, number)
	images = LightField.normalizeImages(images)
	LightField.movingApertureVideo(LabFiles.output(7, 3, name + '-movingAperture', '.avi'), images, aperture, steps)
	LabFiles.show(7, 3, name + '-movingAperture', '.avi')

# getDisplacementVideo('matrioska', 9, 4, np.arange(-1.5, 2.1, 0.1))
# getDisplacementVideo('motorbike', 9, 4, np.arange(-2.0, 0, 0.1))
getDisplacementVideo('building', 17, 4, np.arange(-1.5, 0.5, 0.1))

# getMovingApertureVideo('building', 17, 5, np.arange(0, 1, 1))
