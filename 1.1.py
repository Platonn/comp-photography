from PIL import Image
from lib.Demosaicer import Demosaicer

image_in = Image.open('../Lab2/lighthouse_RAW_noisy_sigma0.01.png')

demosaicer = Demosaicer(image_in)
demosaicer.show()


