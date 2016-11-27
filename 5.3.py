import cv2
from LabFiles import *
from lib.utils.Normalizer import *
from lib.utils.Timer import *
from lib.Relighter import *

def readKnight():
	def withLeadingZeros(number):
		return "%03d" % (number,)

	def getFileName(number):
		result = LabFiles.input(5, 3, 'knight-prefix') + withLeadingZeros(number) + '.resized.png'
		# print result
		return result

	Timer.start('readKnight')
	iStep = 1
	iStart, iEnd = 0, 252
	resImages = []

	# Read images:
	for i in range(iStart, iEnd + 1, iStep):
		# print i
		image = cv2.imread(getFileName(i)).astype(np.float32)
		resImages.append(image)

	# Read directions:
	with open(LabFiles.input(5,3,'light-directions')) as f:
		lines = f.readlines()
		lines = [ line.strip().split(':')[1].split(' ') for line in lines ]
		dirs = [ (float(line[1]), float(line[2]), float(line[3])) for line in lines]
		# print dirs[0] #spike
		resDirs = dirs

	with open(LabFiles.input(5,3,'light-intensities')) as f:
		lines = f.readlines()
		lines = [ line.strip().split(' ') for line in lines ]
		intens = [ (float(line[1]), float(line[2]), float(line[3])) for line in lines]
		# print intens[0] #spike
		resIntens = intens

	resImages = np.array(resImages)
	resDirs = np.array(resDirs)
	resIntens = np.array(resIntens)

	Timer.stop('readKnight')
	return resImages, resDirs, resIntens



graceProbe = cv2.imread(LabFiles.input(5, 2, 'grace-probe'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
rnlProbe = cv2.imread(LabFiles.input(5, 2, 'rnl-probe'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
uffiziProbe = cv2.imread(LabFiles.input(5, 2, 'uffizi-probe'), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)

images, dirs, intens = readKnight()

graceResult = Relighter.relightImage(images, dirs, intens, graceProbe)
graceResult  = Normalizer.normalize(graceResult )
graceResult = Normalizer.to8bit(graceResult )
cv2.imwrite(LabFiles.output(5, 3, 'knight-grace'), graceResult)

rnlResult = Relighter.relightImage(images, dirs, intens, rnlProbe)
rnlResult  = Normalizer.normalize(rnlResult )
rnlResult = Normalizer.to8bit(rnlResult )
cv2.imwrite(LabFiles.output(5, 3, 'knight-rnl'), rnlResult)

uffiziResult = Relighter.relightImage(images, dirs, intens, uffiziProbe)
uffiziResult  = Normalizer.normalize(uffiziResult )
uffiziResult = Normalizer.to8bit(uffiziResult )
cv2.imwrite(LabFiles.output(5, 3, 'knight-uffizi'), uffiziResult)

LabFiles.show(5, 3, 'knight-grace')