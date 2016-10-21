import os
import time
import cv2

from LabFiles import *
from lib.Demosaicer import *

start_time = time.time()

rawImage = cv2.imread(LabFiles.input(2, 1, 'raw'))
naiveDemosaicer = Demosaicer(rawImage)
naiveDemosaicer.saveOutput(LabFiles.output(2, 1, 'raw-copy'))


end_time = time.time()
print(end_time - start_time)

os.system("xdg-open " + LabFiles.output(2, 1, 'raw-copy'))
