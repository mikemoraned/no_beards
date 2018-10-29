import os
import random
import sys
from collections import defaultdict
from math import floor
from statistics import mean

import PIL
from PIL import Image
from PIL.ImageDraw2 import Draw
from PIL.ImageStat import Stat

base_dir = sys.argv[1]
template_image_file_in = sys.argv[2]
image_file_out = sys.argv[3]

buckets = defaultdict(list)


def bucket_value(pixel):
    return floor(mean(pixel))


for dirpath, dirs, files in os.walk(base_dir):
    for filename in files:
        if filename.endswith(".jpg"):
            input_file = os.path.join(dirpath, filename)
            # print(input_file)
            image = Image.open(input_file)
            image_statistics = Stat(image)
            bucket = bucket_value(image_statistics.mean)
            buckets[bucket].append(image)

for bucket in sorted(buckets.keys()):
    images = buckets[bucket]
    print("{}: {}".format(bucket, len(images)))

template_image = Image.open(template_image_file_in)
grid = (40, 30)
scaled_template_image = template_image.resize(grid, resample=PIL.Image.BICUBIC)

base_width, base_height = (180, 200)
grid_width, grid_height = grid

final_image_size = (grid_width * base_width, grid_height * base_height)
final_image = Image.new('RGB', final_image_size, (0, 0, 0))

random.seed(1)

min_bucket, max_bucket = min(buckets.keys()), max(buckets.keys())
bucket_range = max_bucket - min_bucket

for grid_x in range(0, grid_width):
    for grid_y in range(0, grid_height):
        pixel = scaled_template_image.getpixel((grid_x, grid_y))
        bucket = bucket_value(pixel)
        scaled_bucket = floor(((bucket / 255) * bucket_range) + min_bucket)
        print(bucket, scaled_bucket)
        while scaled_bucket not in buckets:
            scaled_bucket += 1
            print(bucket, scaled_bucket)
        images = buckets[scaled_bucket]
        image = random.choice(images)
        final_image.paste(image, (grid_x * base_width,
                                  grid_y * base_height))

final_image.save(image_file_out)
