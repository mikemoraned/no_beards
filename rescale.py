import sys

import PIL
from PIL import Image

image_file_in = sys.argv[1]
image_file_out = sys.argv[2]

image = Image.open(image_file_in)

grid = (40, 30)

scaled = image.resize(grid, resample=PIL.Image.BICUBIC)
scaled.save(image_file_out)
