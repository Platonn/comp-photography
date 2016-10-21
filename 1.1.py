from LabFiles import *
from lib.NaiveDemosaicer import *
from lib.utils.Timer import *

Timer.start('program')

# read file
rawImage = cv2.imread(LabFiles.input(1, 1, 'raw'))
naiveDemosaicer = NaiveDemosaicer(rawImage)
naiveDemosaicer.saveOutput(LabFiles.output(1, 1, 'raw-copy'))

# demosaic
naiveDemosaicer.run()

# save input
naiveDemosaicer.saveOutput(LabFiles.output(1, 1, 'naive'))

# stoper
Timer.stop('program')

# show
LabFiles.show(1, 1, 'naive')