"""
Taken from http://lmfit.github.io/lmfit-py/

Acknowledgements for

Matthew Newville wrote the original version and maintains the project.
Till Stensitzki wrote the improved estimates of confidence intervals, and
    contributed many tests, bug fixes, and documentation.
Daniel B. Allan wrote much of the high level Model code, and many
    improvements to the testing and documentation.
Antonino Ingargiola wrote much of the high level Model code and provided
    many bug fixes.
J. J. Helmus wrote the MINUT bounds for leastsq, originally in
    leastsqbounds.py, and ported to lmfit.
E. O. Le Bigot wrote the uncertainties package, a version of which is used
    by lmfit.
Michal Rawlik added plotting capabilities for Models.
A. R. J. Nelson added differential_evolution, and greatly improved the code
    in the docstrings.

Additional patches, bug fixes, and suggestions have come from Christoph
    Deil, Francois Boulogne, Thomas Caswell, Colin Brosseau, nmearl,
    Gustavo Pasquevich, Clemens Prescher, LiCode, and Ben Gamari.

The lmfit code obviously depends on, and owes a very large debt to the code
in scipy.optimize.  Several discussions on the scipy-user and lmfit mailing
lists have also led to improvements in this code.
"""
"""
Lmfit allows to choose various constraints on fitting parameters
and gives nice outputs of the data. It is not used as before though,
since Gaussian fitting is done only for visualization purposes and
is not involved in calculations. Same was done without this library
"""

import numpy as np
import pylab as pl
from scipy.optimize import leastsq
from lmfit import minimize, Parameters, Parameter,\
                    report_fit, Model
from lmfit.models import PolynomialModel, GaussianModel, ConstantModel, RectangleModel


def polynomial(y, p):
    c0, c1, c2, c3, c4, c5 = p    
    return c0 + c1*y + c2*(y**2) + c3*(y**3) + c4*(y**4) + c5*(y**5)


def gaussian(x, amplitude, center, sigma, offset):
    return (amplitude/np.sqrt(2*np.pi)*sigma) * np.exp(-(x - center)**2/(2*sigma**2)) + offset


def MTF(Y, X, obtain_mtf_at, path):
    """
    Fit a polynomial to the MTF curve
    Fails for scattered data - useless
    """
    poly_mod = PolynomialModel(6)
     
    pars = poly_mod.guess(Y, x=X)
    model = poly_mod
     
    result = model.fit(Y, pars, x=X)
     
    c0 = result.best_values['c0']
    c1 = result.best_values['c1']
    c2 = result.best_values['c2']
    c3 = result.best_values['c3']
    c4 = result.best_values['c4']
    c5 = result.best_values['c5']
    
    params = [c0, c1, c2, c3, c4, c5]

    # Produce a table with values of contrast vs resolution
    if path != False:
        f = open(path + 'contrast_vs_distance.txt', 'w')
        for contrast in range(0, 20):
            resolution = polynomial(contrast, params)
            value = [contrast, resolution]

            f.write(repr(value)+ '\n')
        f.close()
    
    resolution = polynomial(obtain_mtf_at, params)
       
    return result.best_fit, resolution


def GaussConst(signal, guess):
    """
    Fits a Gaussian function
    Plots fwhm and 2*sigma gap widths for comparison
    with the analytically calculated one
    """
    amp, centre, stdev, offset = guess
    
    data = np.array([range(len(signal)), signal]).T
    X = data[:,0]
    Y = data[:,1]

    gauss_mod = GaussianModel(prefix='gauss_')
    const_mod = ConstantModel(prefix='const_')
    
    pars = gauss_mod.make_params(center=centre, sigma=stdev, amplitude=amp)
    pars += const_mod.guess(Y, x=X)
    pars['gauss_center'].min = centre - 5.
    pars['gauss_center'].max = centre + 5.
    pars['gauss_sigma'].max = stdev + 5.
    
    mod = gauss_mod + const_mod
    result = mod.fit(Y, pars, x=X)
    
    fwhm = result.best_values['gauss_sigma'] #* 2.3548
    centr = result.best_values['gauss_center']
    
    # Values within two stdevs i.e. 95%
    pl.plot(np.repeat(centr - fwhm * 2, len(Y)),
            np.arange(len(Y)), 'b-')
    pl.plot(np.repeat(centr + fwhm * 2, len(Y)),
            np.arange(len(Y)), 'b-', label="Sigma * 2")
    
    pl.plot(np.repeat(centr - fwhm * 2.3548 / 2., len(Y)),
            np.arange(len(Y)), 'y--')
    pl.plot(np.repeat(centr + fwhm * 2.3548 / 2., len(Y)),
            np.arange(len(Y)), 'y--', label="FWHM")
    
    return X, result.best_fit, result.best_values['gauss_sigma'] * 4, centr


def Box(signal, guess):
    """
    Fits a box function
    """
    amp, centre, stdev, offset = guess
    
    data = np.array([range(len(signal)), signal]).T
    X = data[:,0]
    Y = data[:,1]

    gauss_mod = RectangleModel(prefix='gauss_', mode='logistic')
    const_mod = ConstantModel(prefix='const_')
    
    pars = gauss_mod.make_params( center1=centre-stdev*3, center2=centre+stdev*3, sigma1=0, sigma2=0, amplitude=amp)
    pars += const_mod.guess(Y, x=X)
    pars['gauss_center1'].min = centre-stdev*3 - 3
    pars['gauss_center2'].max = centre-stdev*3 + 3
    pars['gauss_center2'].min = centre+stdev*3 - 3
    pars['gauss_center2'].max = centre+stdev*3 + 3
    
    mod = gauss_mod + const_mod
    result = mod.fit(Y, pars, x=X)
    
    c1 = result.best_values['gauss_center1']
    c2 = result.best_values['gauss_center2']
    
    pl.legend()
    
    return X, result.best_fit, c2-c1
