# k2ucd
K2 Ultracool Dwarfs astronomy working software

This is just some working software for the K2 Ultracool Dwarfs survey (PI Gizis).  General strategy is:

[Not here:] Rishi Paudel (University of Delaware) graduate student creates PSF photoometry and corrects with K2SC
 all data stored on a common Google Drive.^1,2,3 

*This software* Read files, use periodograms to identify rotation periods. More to come

[Not here:] Independent process: Jingbao Ji (U. Delaware) transit search on same data.

import k2ucd.py 

Makes use of astropy: http://www.astropy.org/  Citing: http://www.astropy.org/acknowledging.html 

New astropy paper: http://adsabs.harvard.edu/abs/2018arXiv180102634T still under review, so cite:

First astropy paper: http://adsabs.harvard.edu/abs/2013A%26A...558A..33A

Not likely to be of use to anyone else. 


1: For how to do this, see Ann Marie Cody's tutorial: https://github.com/amcody/K2tutorials/blob/master/notebooks/K2psftutorial.ipynb

2: PyKE tools see http://pyke.keplerscience.org/  Citations here: http://pyke.keplerscience.org/citing.html 

3: K2SC is found by https://github.com/OxES/k2sc. Remember to cite authors: http://adsabs.harvard.edu/abs/2016MNRAS.459.2408A
