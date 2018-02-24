import numpy as np
#import matplotlib as mpl
import glob
import k2ucd
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
filelist = open('c14list.txt', 'r') # 'r' = read
#lines = filelist.readlines()
for myline in filelist:
    # grab the EPIC name
    k2name=myline.strip()
    #print(k2name)
    ispot_epic=k2name.find('EPIC')
    epic_number=k2name[ispot_epic+5:ispot_epic+5+epic_length]
    #print(epic_number)
    #
    # rad the data
    dates,flux,flux_pcor,flux_ptcor,mflags = k2ucd.readpsfk2cor(k2name)
    # compute best fitting frequency in Lomb-Scargle Periodogram
    frequency,power,best_frequency,best_fap=k2ucd.periodcheck(dates,flux_pcor,mflags)
    #
    # now let's do it again, but with the position and time corrected version
    freq_pt,power_pt,best_pt_frequency,best_pt_fap=k2ucd.periodcheck(dates,flux_ptcor,mflags)
    #
    #print(best_frequency)
    print('{0:8.5f} {1:8.4f} {2:12.4e} {3:8.4f} {4:12.4e} {5}'.format(1.0/best_frequency,24.0/best_frequency,best_fap,
                                                       24.0/best_pt_frequency,best_pt_fap,epic_number))
#
filelist.close()
