#!/usr/bin/python

'''
this script grabs EDR .IMG PDS products of MRO HiRISE, 
based on the knowledge of the image identifier/filename root of one
image of a known stereo pair (e.g. "ESP_011277_1825").

USAGE: python EDR_grab.py <HIRISE_PRODUCT_ID>
'''

import urllib2
from BeautifulSoup import BeautifulSoup
import os
import sys
import subprocess
 
def betweenstring(string,a,b):
    list = []
    stringsplit = string.split(a)
    if stringsplit != []:
        for item in stringsplit[1:]:
            nr = item.find(b)
            if nr != -1:
                list.append(item.split(b)[0])
    return list
 
usage = "USAGE: python EDR_grab.py <EDR root of a pair \n e.g. python EDR_grab.py ESP_011277_1825"

if len(sys.argv) == 1:
    print usage
    sys.exit()
else:    
    root_edr1 = sys.argv[1]

url ="http://hirise.lpl.arizona.edu/"+ root_edr1

os.chdir(".")

# read url content into ascii text
baseurl = os.path.dirname(url)
req = urllib2.urlopen(url)
data = req.read()
 
# get 'EDR products' link
soup = BeautifulSoup(data)
for tag in soup.findAll(lambda tag: (tag.name == 'a' and tag.text == 'EDR products'), href=True):
    edrurl1 = str(tag['href'])
 
# get stereo pair link
stereo = betweenstring(data,"This is a stereo pair with <strong>","</strong>")[0]
soup = BeautifulSoup(stereo)
href = soup.findAll('a')
stereopair = href[0]['href']
 
# stereo pair url
url = baseurl + '/' + str(stereopair)
 
# read stereo pair url content into ascii text
req = urllib2.urlopen(url)
data = req.read()
 
# get 'EDR products' link for stereo pair
soup = BeautifulSoup(data)
for tag in soup.findAll(lambda tag: (tag.name == 'a' and tag.text == 'EDR products'), href=True):
    edrurl2 = str(tag['href'])
 
# print out the contents of the edrurl1 folder
req = urllib2.urlopen(edrurl1)
data = req.read()
edrlist1=open('./edr-list1.txt', 'w+')
soup = BeautifulSoup(data)
for tag in soup.findAll('a'):
    print >> edrlist1, edrurl1+ str(tag['href'])
print "EDR-URL-1 is: ",  edrurl1
edr1root = edrurl1[-16:-1]
print "EDR-ROOT-1 is: ", edr1root
edrlist1.close()

# print out the contents of the edrurl2 folder
req = urllib2.urlopen(edrurl2)
data = req.read()
soup = BeautifulSoup(data)
edrlist2=open('./edr-list2.txt', 'w+')
for tag in soup.findAll('a'):
    print >> edrlist2, edrurl2 + str(tag['href'])
print "EDR-URL-2 is: ", edrurl2
edr2root = edrurl2[-16:-1]
print "EDR-ROOT-1 is: ", edr2root
edrlist2.close()

# 1st image of pair RED wget list
os.chdir(".")
with open('./edr-list1.txt', 'r') as oldfile:
    with open(edr1root + '.txt', 'w') as newfile:
        content = oldfile.readlines()
        for line in content:
            if 'RED' in line:
                newfile.write(line)
            else:
                print "no RED"
    newfile.close()
oldfile.close()

# 2nd image of pair RED wget list
os.chdir(".")
with open('./edr-list2.txt', 'r') as oldfile:
    with open(edr2root + '.txt', 'w') as newfile:
        content = oldfile.readlines()
        for line in content:
            if 'RED' in line:
                newfile.write(line)
            else:
                print "no RED"
    newfile.close()
oldfile.close()

# wget EDR of both (for the time being in the cwd)
edrwget1 = edr1root + '.txt'
edrwget2 = edr2root + '.txt'

os.chdir(".")
with open('./edr_root.txt', 'w') as namefile:
    namefile.write(edr1root+'\n')
    namefile.write(edr2root)
namefile.close()

os.chdir(".")
with open(edrwget1) as wgetsource:
    for line in wgetsource:
       cmd = 'wget '+ line
       output = subprocess.call(cmd, stdout=subprocess.PIPE, shell=True)
wgetsource.close()

with open(edrwget2) as wgetsource:
    for line in wgetsource:
       cmd = 'wget '+ line
       output = subprocess.call(cmd, stdout=subprocess.PIPE, shell=True)
wgetsource.close()


print "EDR RED downloads finished. Ready for Hieadr2mosaic"
