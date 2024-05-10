# BEM 1/8/24

# Uses python package at: https://github.com/luke-a-brown/hemipy

import exifread
import glob
import hemipy
import os
import numpy as np

from project_functions import check_dates

# define input directory (sub-directories correspond to measurement plots and contain images from that plot)
input_dir = "/media/bem/data/NEON/raw_hemisphere_photos"
# define latitude of the site (necessary for FIPAR computation)
lat = 19.55309

# define image size and optical centre
img_size = np.array([120, 160])
opt_cen = np.array([60, 80])
# define calibration function coefficients (^3, ^2 and ^1)
cal_fun = np.array([0, 0, 0.0548543])

# calculate the zenith and azimuth angle of each pixel
zenith = hemipy.zenith(img_size, opt_cen, cal_fun)
azimuth = hemipy.azimuth(img_size, opt_cen)

# open output file and write header
output_file = open('dhp_output.csv', 'w')
output_file.write(
    'date, plot, direction, PAIe_hinge, PAI_hinge, clumping_hinge,'
    'PAIe_Miller, PAI_Miller, Clumping_Miller, FIPAR, FCOVER\n'
)

# locate and loop through measurement plots
plots = glob.glob(input_dir + '/*')

for i in range(len(plots)):

    print("PLOT: " + os.path.basename(plots[i]))
    layers = glob.glob(plots[i] + '/*')

    # locate and loop through understory/overstory layers
    for j in range(len(layers)):

        print("LAYER: " + os.path.basename(layers[j]))
        # check EXIF to see if everything has the same date
        if not check_dates(layers[j]):
            raise ValueError("dates are not the same in layer EXIF")
        # open first image in folder and retrieve date and time from EXIF data
        image = open(glob.glob(layers[j] + '/*')[0], 'rb')
        tags = exifread.process_file(image)
        # check the height/width against the constants
        if not str(tags['Image ImageLength']) == str(img_size[0]):
            raise ValueError("image height from EXIF does not match height parameter")
        if not str(tags['Image ImageWidth']) == str(img_size[1]):
            raise ValueError("image width from EXIF does not match width parameter")
        # determine date of plot acquisition
        date = str(tags['EXIF DateTimeOriginal'])[0:10].replace(':', '-')

        # determine image direction
        if 'overstory' in layers[j]:
            direction = 'up'
        elif 'understory' in layers[j]:
            direction = 'down'

        # run the main function and write results to output file
        results = hemipy.process(layers[j], zenith, azimuth, date=date, lat=lat, direction=direction)
        output_file.write(date + ',' + \
                          layers[j].split('\\')[-2] + ',' + \
                          direction + ',' + \
                          str(results['paie_hinge']) + ',' + \
                          str(results['pai_hinge']) + ',' + \
                          str(results['clumping_hinge']) + ',' + \
                          str(results['paie_miller']) + ',' + \
                          str(results['pai_miller']) + ',' + \
                          str(results['clumping_miller']) + ',' + \
                          str(results['fipar']) + ',' + \
                          str(results['fcover']) + '\n')

        # close output file
        output_file.close()
