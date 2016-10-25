from LabFiles import *
from lib.EdgeAwareDemosicer import *
from lib.utils.Timer import *

Timer.start('program')

# read file
rawImage = cv2.imread(LabFiles.input(1, 2, 'raw'))
edgeAwareDemosaicer = EdgeAwareDemosaicer(rawImage)

# process
edgeAwareDemosaicer.run()

# save input
edgeAwareDemosaicer.saveOutput(LabFiles.output(1, 2, 'edge-aware'))

# stoper
Timer.stop('program')

# show
LabFiles.show(1, 2, 'edge-aware')