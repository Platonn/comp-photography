import cv2
from LabFiles import *
from lib.utils.Normalizer import *
from lib.utils.Timer import *
from lib.Relighter import *

def readTeapots():
	def getFileName((theta, phi)):
		return LabFiles.input(5, 2, 'teapots-prefix') + str(theta) + '_' + str(phi) + '.png'

	Timer.start('readTeapots')
	phiStep = 30
	thetaStep = 45
	phiStart, phiEnd = -60, 60
	thetaStart, thetaEnd = 0, 315
	resImages = []
	resDirs = []
	resIntens = []

	for phi in range(phiStart, phiEnd + 1, phiStep):
		for theta in range(thetaStart, thetaEnd + 1, thetaStep):
			radTheta, radPhi = Relighter.deg2rad((theta, phi))  ############## SPIKE - casting deg to rad!!!!!!!!!!!!!!!!!!!!!
			image = cv2.imread(getFileName((theta, phi))).astype(np.float32)
			resImages.append(image)
			DxDyDz = Relighter.thetaPhi2DxDyDz((radTheta, radPhi))
			resDirs.append(DxDyDz)
			resIntens.append(np.array([1., 1., 1.]))

	resImages = np.array(resImages)
	resDirs = np.array(resDirs)
	resIntens = np.array(resIntens)

	Timer.stop('readTeapots')
	return resImages, resDirs, resIntens



graceProbe = cv2.imread(LabFiles.input(5, 2, 'grace-probe'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
rnlProbe = cv2.imread(LabFiles.input(5, 2, 'rnl-probe'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
uffiziProbe = cv2.imread(LabFiles.input(5, 2, 'uffizi-probe'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)

images, dirs, intens = readTeapots()

# graceResult = Relighter.relightImage(images, dirs, intens, graceProbe)
# graceResult  = Normalizer.normalize(graceResult )
# graceResult = Normalizer.to8bit(graceResult )
# cv2.imwrite(LabFiles.output(5, 2, 'teapots-grace'), graceResult)
#
# rnlResult = Relighter.relightImage(images, dirs, intens, rnlProbe)
# rnlResult  = Normalizer.normalize(rnlResult )
# rnlResult = Normalizer.to8bit(rnlResult )
# cv2.imwrite(LabFiles.output(5, 2, 'teapots-rnl'), rnlResult)
#
# uffiziResult = Relighter.relightImage(images, dirs, intens, uffiziProbe)
# uffiziResult  = Normalizer.normalize(uffiziResult )
# uffiziResult = Normalizer.to8bit(uffiziResult )
# cv2.imwrite(LabFiles.output(5, 2, 'teapots-uffizi'), uffiziResult)

Relighter.relightVideo(LabFiles.output(5, 4, 'teapot-grace-video', '.avi'), 1000, 10, images, dirs, intens, graceProbe)

LabFiles.show(5, 2, 'teapots-grace')
LabFiles.show(5, 4, 'teapots-grace-video', '.avi')