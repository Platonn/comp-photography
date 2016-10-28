from LabFiles import *
from lib.ChrominanceMedianFilterer import *
from lib.utils.Timer import *
from lib.GammaCorrector import *
from lib.NaiveDemosaicer import *

Timer.start('program')

# read file
seashoreImage = cv2.imread(LabFiles.input(1, 5, 'raw'))

# process
naiveDemasaicer = NaiveDemosaicer(seashoreImage)
naiveDemasaicer.run()

naiveDemasaicer.saveOutput(LabFiles.output(1, 5, 'raw-colors'))

# stoper
Timer.stop('program')

# show
LabFiles.show(1, 5, 'raw-colors')