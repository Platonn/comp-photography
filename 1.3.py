from LabFiles import *
from lib.EdgeAwareDemosicer import *
from lib.utils.Timer import *

Timer.start('program')

# read file
edgeAwareImage = cv2.imread(LabFiles.output(1, 2, 'edge-aware'))

# process
GammaCorrector(2.2).run(edgeAwareImage)

# save input
cv2.imwrite(LabFiles.output(1, 3, 'edge-aware-gamma'), edgeAwareImage)


# stoper
Timer.stop('program')

# show
LabFiles.show(1, 3, 'edge-aware-gamma')