
def check_dates(img_dir):

    import glob
    import exifread

    out = ""
    imgs = glob.glob(img_dir + "/*")

    for i in range(len(imgs)):

        ii = open(imgs[i], 'rb')
        i0 = exifread.process_file(ii)
        d0 = str(i0['EXIF DateTimeOriginal'])[0:10].replace(':', '-')
        out += d0

    return out
