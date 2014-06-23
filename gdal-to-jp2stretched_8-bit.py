#!/usr/bin/python

'''
converts a gdal-edible 1-band file (intended to be e.g. a floating point ISIS3 .cub)
to jpeg2000 and stretches it to 8 bits using min/max. It require GDAL with bindings
and some other stuff. the argument is the extension withouth leading "."

USAGE:
python gdal-to-jp2stretched_8-bit.py <extension without DOT>

e.g.
python gdal-to-jp2stretched_8-bit lev2.cub

or:
python gdal-to-jp2stretched_8-bit cub
'''

# USAGE python CTX_lev2_processing.py <MAP_TEMPLATE>
import sys
import os
import glob
import subprocess
import shutil
import gdal

# USAGE ./ cub-go-jp2stretched_v0.2.py [extension without DOT] e.g.
#       ./ cub-go-jp2stretched_v0.2.py lev2.cub

extension = sys.argv[1]

# create output directory
if not os.path.exists("./output"):
	os.makedirs("./output")

# loop through files
os.chdir(".")

for filename in glob.glob("*." + extension):
        try:
                print "processing: ", filename
                #print os.path.basename(filename)
                filename_root = filename.split(".")[-2]
                out_jp2 = filename_root+'.jp2'
                out_jp2_xml = filename_root+'.jp2.aux.xml'
                # gdal_translate
                try:
                        #gdal part
                        image=gdal.Open(filename)
                        band = image.GetRasterBand(1)
                        #
                        print 'Band Type=',gdal.GetDataTypeName(band.DataType)
                        bmin = band.GetMinimum()
                        bmax = band.GetMaximum()
                        if bmin is None or bmax is None:
                                (bmin,bmax) = band.ComputeRasterMinMax(1)
                        print 'Min=%.3f, Max=%.3f' % (bmin,bmax)
                        sbmin = str(bmin)
                        sbmax = str(bmax)
                        #
                        print band
                        #end gdal part
                        cmd = 'gdal_translate ' + filename + ' -scale ' + sbmin + ' ' + sbmax +' 1 255 -a_nodata 0 -ot Byte -of JPEG2000 ' + out_jp2
                        output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]
                        print cmd
                except:
                        print "Oops!", cmd
                # mv to output 
                try:
                        source = './'+ out_jp2
                        destination = './output/'+ out_jp2
                        print "source is: " + source
                        print "destination is: " + destination
                        src_file = os.path.join(".", our_jp2)
                        src_file2 = os.path.join(".", out_jp2_xml)
                        dst_file = os.path.join("./output/", out_jp2)
                        dst_file2 = os.path.join("./output/", out_jp2_xml)
                        shutil.move(src_file, dst_file)
                        shutil.move(src_file2, dst_file2)
                except OSError as e:
                        print "Oops!"                       
        except: 
                print "Ooops! Unexpected error: Loop continues"
print "Done."
