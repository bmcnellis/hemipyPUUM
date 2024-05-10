# BEM May 2024

# Purpose: downloads NEON hemispherical files and arranges them according to the requirements of the hemipy package

from urllib.request import urlretrieve

import os
import pandas

proc_dir = "/media/bem/data/NEON/raw_hemisphere_photos"
df = pandas.read_csv("dhp_perimagefile.csv")

for i in range(1, len(df.index)):

    # Debug break:

    # Files:
    f_URL = df.loc[i, 'imageFileUrl']
    f_fnm = os.path.splitext(df.loc[i, 'imageFileName'])[0]

    # Directory structure:
    i_pl = df.loc[i, 'plotID']
    i_tp = df.loc[i, 'imageType']

    if i_tp not in ["overstory", "understory"]:
        continue

    if not os.path.isdir(os.path.join(proc_dir, i_pl)):
        os.mkdir(os.path.join(proc_dir, i_pl))

    if not os.path.isdir(os.path.join(proc_dir, i_pl, i_tp)):
        os.mkdir(os.path.join(proc_dir, i_pl, i_tp))

    # REQUIRED DIRECTORY STRUCTURE:
    # example_data
    #     plot_a
    #         overstory
    #             image_1, image_2, ..., image_14, image_15
    #         understory
    #             image_1, image_2, ..., image_14, image_15

    # Put it all together
    f_out = os.path.join(proc_dir, i_pl, i_tp, f_fnm + ".TIFF")

    print("FILE:" + f_out)

    # REQUIRED DIRECTORY STRUCTURE:
    # example_data
    #     plot_a
    #         overstory
    #             image_1, image_2, ..., image_14, image_15
    #         understory
    #             image_1, image_2, ..., image_14, image_15

    # Only run if the output file is not present
    if not os.path.isfile(f_out):
        urlretrieve(f_URL, f_out)
        print("dl OK")
    else:
        print("dl NO")
