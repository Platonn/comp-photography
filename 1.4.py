from LabFiles import *
from lib.ChrominanceMedianFilterer import *
from lib.utils.Timer import *

Timer.start('program')

# read file
naiveImage = cv2.imread(LabFiles.output(1, 1, 'naive'))
chrominanceMedianFilterer = ChrominanceMedianFilterer(naiveImage)

# process
chrominanceMedianFilterer.run()
chrominanceMedianFilterer.saveOutput(LabFiles.output(1, 4, 'naive-medianFilter'))

chrominanceMedianFilterer.correctGamma()
chrominanceMedianFilterer.saveOutput(LabFiles.output(1, 4, 'naive-medianFilter-gamma'))
# stoper
Timer.stop('program')

# show
LabFiles.show(1, 4, 'naive-medianFilter-gamma')