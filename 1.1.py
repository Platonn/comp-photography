import os
import time

from PIL import Image
from lib.NaiveDemosaicer import NaiveDemosaicer

start_time = time.time()
filename_in ='../Lab2/lighthouse_RAW_noisy_sigma0.01.png'
filename_out_load_rgb = "../out_1.1-load_rgb.png"
filename_out_demosaic = "../out_1.1-demosaic.png"


image_in = Image.open(filename_in)

demosaicer = NaiveDemosaicer(image_in)
demosaicer.load_rgb()
demosaicer.save(filename_out_load_rgb)

demosaicer.demosaic()
demosaicer.merge_monochrom_images()
demosaicer.save(filename_out_demosaic)

end_time = time.time()
print(end_time - start_time)

#os.system("xdg-open " + filename_out_load_rgb)
os.system("xdg-open " + filename_out_demosaic)
