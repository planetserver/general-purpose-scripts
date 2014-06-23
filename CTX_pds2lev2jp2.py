#!/usr/bin/python

'''
The script processes MRO Context Camera (CTX) EDR 
from PDS .IMG to level2 .cub and outputs
stretched 8 bit jp2.

# USAGE python CTX_pds2lev2jp2.py <MAP_TEMPLATE>
e.g. 
python CTX_pds2lev2jp2 map_template.map 
'''

import sys
import os
import glob
import subprocess
import shutil
import gdal

maptemplate = sys.argv[1]

# create output directory
if not os.path.exists("./output"):
	os.makedirs("./output")

# loop through files
os.chdir(".")

for filename in glob.glob("*.IMG"):
        try:
                print "processing: ", filename
                ctx_root = filename.split(".")[-2]
                ctx_lev0 = ctx_root+'.lev0.cub'
                ctx_lev1 = ctx_root+'.lev1.cub'
                ctx_lev1eo = ctx_root+'.lev1eo.cub'
                ctx_lev2 = ctx_root+'.lev2.cub'
                ctx_jp2 = ctx_root+'.jp2'
                ctx_jp2_xml = ctx_root+'.jp2.aux.xml'
                # mroctx2isis
                try:
                        cmd = 'mroctx2isis from='+ filename +' to='+ ctx_lev0
                        output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]
                        print cmd
                except:
                        print "Oops!", cmd
                # spiceinit
                try:
                        cmd = 'spiceinit from='+ ctx_lev0
                        output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]
                        print cmd
                except:
                        print "Oops!", cmd
                # ctxcal
                try:
                        cmd = 'ctxcal from=' + ctx_lev0 + ' to=' + ctx_lev1
                        output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]
                        print cmd
                except:
                        print "Oops!", cmd
                # ctxevenodd
                try:
                        cmd = 'ctxevenodd from=' + ctx_lev1 + ' to=' + ctx_lev1eo
                        output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]
                        print cmd
                except:
                        print "Oops!", cmd
                # cam2map
                try:
                        cmd = 'cam2map from=' + ctx_lev1eo + ' to=' + ctx_lev2 + ' map=' + maptemplate + " pixres=map"
                        output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]
                        print cmd
                except:
                        print "Oops!", cmd
                # gdal_translate
                try:
                        #gdal part
                        image=gdal.Open(ctx_lev2)
                        band = image.GetRasterBand(1)
                        print 'Band Type=',gdal.GetDataTypeName(band.DataType)
                        bmin = band.GetMinimum()
                        bmax = band.GetMaximum()
                        if bmin is None or bmax is None:
                                (bmin,bmax) = band.ComputeRasterMinMax(1)
                        print 'Min=%.3f, Max=%.3f' % (bmin,bmax)
                        sbmin = str(bmin)
                        sbmax = str(bmax)
                        print band
                        cmd = 'gdal_translate ' + ctx_lev2 + ' -scale ' + sbmin + ' ' + sbmax +' 1 255 -a_nodata 0 -ot Byte -of JPEG2000 ' + ctx_jp2
                        output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]
                        print cmd
                except:
                        print "Oops!", cmd
                # mv to output 
                try:
                        os.remove(ctx_lev0)
                except OSError as e:
                        print "Oops!"
                try:
                        os.remove(ctx_lev1)
                except OSError as e:
                        print "Oops!"
                try:
                        os.remove(ctx_lev1eo)
                except OSError as e:
                        print "Oops!"
                try:
                        source = './'+ ctx_jp2
                        destination = './output/'+ ctx_jp2
                        print "source is: " + source
                        print "destination is: " + destination
                        src_file = os.path.join(".", ctx_jp2)
                        src_file2 = os.path.join(".", ctx_jp2_xml)
                        dst_file = os.path.join("./output/", ctx_jp2)
                        dst_file2 = os.path.join("./output/", ctx_jp2_xml)
                        shutil.move(src_file, dst_file)
                        shutil.move(src_file2, dst_file2)
                except OSError as e:
                        print "Oops!"                       
        except: 
                print "Ooops! Unexpected error: Loop continues"
                # os.remove(ctx_lev2)
                # os.remove(ctx_lev0)
print "Done."
