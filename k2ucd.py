import numpy as np
import matplotlib.pyplot as plt

# uses astropy
import astropy.io.ascii as ascii
from astropy.table import Table
from astropy.io import fits
from astropy.stats import LombScargle
from astropy.stats import sigma_clipped_stats

#

#
def readpsfk2cor(k2name):
    tbl = Table.read(k2name)
    dates = tbl['time']
    quality = tbl['quality']
    flux = tbl['flux']
    fluxerr = tbl['error']
    # warning: these errors are wrong
    trendt = tbl['trtime']
    mflags = tbl['mflags']
    trendp = tbl['trposi']
    xpos = tbl['x']
    ypos = tbl['y']
    #trendt = tbl['trtime']
    flux_pcor = flux-trendp+np.nanmedian(trendp)
    flux_ptcor= flux-trendp+np.nanmedian(trendp)-trendt+np.nanmedian(trendt)
    return dates,flux,flux_pcor,flux_ptcor,mflags
#
def adderrors(flux_ptcor,mflags):
    # the errors from the PSF photometry are no good, so use robust standard dev
    #  This has no real statistic basis and indeed is obviously fudged.
    #  Plus, These are still likely still overestimated since periodic signals aren't modeled
    ig = (mflags==0)
    rmean,rmedian,rstd=sigma_clipped_stats(flux_ptcor[ig], sigma=3, iters=5)
    #rstd=np.std(flux_ptcor)
    flux_errors= flux_ptcor*0.0 + rstd
    return flux_errors
#
def periodcheck(thistime,thisflux,mflags):
    #dates,flux,flux_pcor,flux_ptcor,mflags = readpsfk2cor(k2name)
    ig = (mflags==0)
    #
    # k2sc documentation:
    # https://github.com/OxES/k2sc/blob/master/relase_readme.txt
    # indicates that mflags ==0 would be good data.  
    #
    # This section, not used, shows how to do sigma clipping. Unncessary since mgflags already
    # applies a ~4-5 sigma clip.  
    #sigma clipping stuff ; see http://docs.astropy.org/en/stable/stats/robust.html#sigma-clipping
    #from astropy.stats import sigma_clip
    #filtered_data = sigma_clip(flux_ptcor, sigma=3, iters=10)
    # that would be a mask
    #
    # DISCOVERY: WILL CRASH IF ALL DATA FLAGGED AS BAD!!!
    # SOLUTION: DON'T GIVE IT THOSE FILES! 
    #
    # Periodogram stuff
    # search good data only in period range 1 hour to 10 days
    ls= LombScargle(thistime[ig], thisflux[ig])
    frequency, power = ls.autopower(maximum_frequency=24.0,minimum_frequency=0.1)
    #
    best_frequency = frequency[np.argmax(power)]
    best_fap=ls.false_alarm_probability(power.max())
    #
    # Calculate the model if desired
    #y_fit = ls.model(dates, best_frequency)
    #plt.plot(t_fit,y_fit,'k-')
    #
    return frequency,power,best_frequency,best_fap
#
#  subroutine to loop through all sources of a given campaign.  
def periodloop(cfile):
    # EPIC numbers are 9 digits:
    epic_length=9
    # debugging only:
    #print(cfile)
    # how to read simple ascii file
    #   https://oceanpython.org/2012/12/02/reading-text-ascii-files/
    filelist = open(cfile, 'r') # 'r' = read
    for myline in filelist:
        # grab the EPIC name
        k2name=myline.strip()
        ispot_epic=k2name.find('EPIC')
        epic_number=k2name[ispot_epic+5:ispot_epic+5+epic_length]
        # read the data
        dates,flux,flux_pcor,flux_ptcor,mflags = readpsfk2cor(k2name)
        # compute best fitting frequency in Lomb-Scargle Periodogram
        frequency,power,best_frequency,best_fap=periodcheck(dates,flux_pcor,mflags)
        #
        # now let's do it again, but with the position and time corrected version
        freq_pt,power_pt,best_pt_frequency,best_pt_fap=periodcheck(dates,flux_ptcor,mflags)
        #
        #print(best_frequency)
        print('{0:9.5f} {1:8.4f} {2:12.4e} {3:8.4f} {4:12.4e} {5}'.format(1.0/best_frequency,
                24.0/best_frequency,best_fap,24.0/best_pt_frequency,best_pt_fap,epic_number))
        #
    filelist.close()
