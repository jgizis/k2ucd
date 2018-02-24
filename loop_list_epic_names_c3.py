import numpy as np
#import matplotlib as mpl
import glob
#import k2ucd
#
# Purpose: Run through all data in a directory, compute periodogram and save.
#
# This is the size of an EPIC catalog name
epic_length=9
#
# This glob stuff doesn't work with Google Drive.  Can install other packahge apparently.
#for k2name in glob.glob('/Volumes/GoogleDrive/My?Drive/long_cad_cam14/k2sc_detrended/*'):
#3for k2name in glob.glob("/Volumes/Google*/*/*"):
#
# how to read simple ascii file
#   https://oceanpython.org/2012/12/02/reading-text-ascii-files/
filelist = open('c3list.txt', 'r') # 'r' = read
#lines = filelist.readlines()
for myline in filelist:
    # grab the EPIC name
    k2name=myline.strip()
    #print(k2name)
    ispot_epic=k2name.find('EPIC')
    epic_number=k2name[ispot_epic+5:ispot_epic+5+epic_length]
    print(epic_number)
#
filelist.close()
