import os
import sys
from collections import defaultdict
from math import floor
from statistics import mean

from PIL import Image
from PIL.ImageStat import Stat

base_dir = sys.argv[1]

buckets = defaultdict(list)

for dirpath, dirs, files in os.walk(base_dir):
    for filename in files:
        if filename.endswith(".jpg"):
            input_file = os.path.join(dirpath, filename)
            # print(input_file)
            image = Image.open(input_file)
            image_statistics = Stat(image)
            bucket = floor(mean(image_statistics.mean))
            buckets[bucket].append(image)

for bucket in sorted(buckets.keys()):
    images = buckets[bucket]
    print("{}: {}".format(bucket, len(images)))
