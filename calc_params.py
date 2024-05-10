# BEM 1/8/24

import os, cv2

from pathlib import Path

input_dir = "/media/bem/data/NEON/raw_hemisphere_photos"

dir_1 = os.path.join(input_dir, os.listdir(input_dir)[0])
dir_2 = os.path.join(dir_1, os.listdir(dir_1)[0])
f_1 = os.path.join(dir_2, os.listdir(dir_2)[0])

img = cv2.imread(f_1)

if not img.__class__.__name__ == 'ndarray':
    raise TypeError("cv2 image import failed")

h, w, c = img.shape

print('width:  ', w)
print('height: ', h)
print('channel:', c)
