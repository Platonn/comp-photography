from LabFiles import *
from lib.NaiveDemosaicer import *
from lib.utils.Timer import *

Timer.start('program')

# read file
rawImage = cv2.imread(LabFiles.input(2, 1, 'raw'))
naiveDemosaicer = NaiveDemosaicer(rawImage)

# demosaic
naiveDemosaicer.run()

# save input
naiveDemosaicer.saveOutput(LabFiles.output(2, 1, 'raw-copy'))

# stoper
Timer.stop('program')

# show
LabFiles.show(2, 1, 'raw-copy')