#!/usr/bin/python

import sys
import glob
import subprocess
import os

'''
bzip2 anything with a certain extension in the current directory.

USAGE:
python bzip_me-bit.py <extension without DOT>

e.g.
python bzip_me.py tif
'''

usage = "USAGE: python bzip_me-bit.py <extension without DOT>"

if len(sys.argv) == 1:
    print usage
    sys.exit()
else:    
    root_edr1 = sys.argv[1]
    
extension = sys.argv[1]

os.chdir(".")

for filename in glob.glob("*." + extension):
  print "compressing: ", filename
  try:
    cmd = 'bzip2 '+ filename
    output = subprocess.call(cmd, stdout=subprocess.PIPE, shell=True)
    print cmd
  except:
    print "can't bzip2"

print "compressed all"
