#!/usr/bin/python

import sys
import glob
import subprocess
import os

'''
bunzip2 anything in the current directory.

USAGE:
python bzip_me.py 

'''

os.chdir(".")

for filename in glob.glob("*.bz2"):
  print "uncompressing: ", filename
  try:
    cmd = 'bunzip2 '+ filename
    output = subprocess.call(cmd, stdout=subprocess.PIPE, shell=True)
    print cmd
  except:
    print "can't bunzip2"

print "uncompressed all"
