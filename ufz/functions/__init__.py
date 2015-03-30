#!/usr/bin/env python
"""
    Defines common functions that are used in curve_fit or fmin parameter estimations.

    There are also some common test functions for parameter estimations such as Rosenbrock and Griewank.

    And test functions for parameter sensitivity analysis.


    Defines the functions (except test functions) in two forms (ex. of 3 params):
        1. func(x, p1, p2, p3)
        2. func_p(x, p)  with p[0:3]
    These cost functions can be used for example with curve_fit
        p, cov  = opt.curve_fit(ufz.functions.f1x, x, y, p0=[p0,p1])

    Defines also two cost functions, one with absolute sum, one with squared sum of deviations.
        3. cost_func    sum(abs(obs-func))
        4. cost2_func   sum((obs-func)**2)
    These cost functions can be used for example with fmin
        p = opt.fmin(ufz.functions.cost_f1x, np.array([p1,p2]), args=(x,y), disp=False)
    or
        p, nfeval, rc = opt.fmin_tnc(ufz.functions.cost_f1x, [p1,p2], bounds=[[None,None],[None,None]],
                                     args=(x,y), approx_grad=True, disp=False)

    Note the different argument orders:
    curvefit wants f(x,*args) with the independent variable as the first argument
             and the parameters to fit as separate remaining arguments.
    fmin is a general minimiser with respect to the first argument, i.e. func(p,*args).

    There are also two common cost functions (absolute and squared deviations) where any function
    in the form func(x, p) can be used as second argument:
        5. cost_abs(p, func, x, y)
        6. cost_square(p, func, x, y)
    Used for example as
        p = opt.fmin(ufz.functions.cost_abs, np.array([p1,p2]), args=(ufz.functions.f1x_p,x,y), disp=False)
    or
        p, nfeval, rc = opt.fmin_tnc(ufz.functions.cost_square, [p1,p2], bounds=[[None,None],[None,None]],
                                     args=(ufz.functions.f1x_p,x,y), approx_grad=True, disp=False)


    Definition
    ----------
    Current functions are (there is always the second form with the name appended by _p;
    these are used in the cost functions).

        arrhenius         1 param:  Arrhenius temperature dependence of biochemical rates:
                                    exp((T-TC25)*E/(T25*R*(T+T0))), parameter: E
        f1x               2 params: General 1/x function: a + b/x
        fexp              3 params: General exponential function: a + b * exp(c*x)
        gauss             2 params: Gauss function: 1/(sig*sqrt(2*pi)) *exp(-(x-mu)**2/(2*sig**2)), parameter: mu, sig
        lasslop           6 params: Lasslop et al. (2010) a rectangular, hyperbolic light-response GPP
                                    with Lloyd & Taylor (1994) respiration and the maximum canopy uptake
                                    rate at light saturation decreases exponentially with VPD as in Koerner (1995)
        line0             1 params: Straight line: a*x
        line              2 params: Straight line: a + b*x
        lloyd_fix         2 params: Lloyd & Taylor (1994) Arrhenius type with T0=-46.02 degC and Tref=10 degC
        lloyd_only_rref   1 param:  Lloyd & Taylor (1994) Arrhenius type with fixed exponential term
        logistic          3 params: Logistic function: a/(1+exp(-b(x-c)))
        logistic_offset   4 params: Logistic function with offset: a/(1+exp(-b(x-c))) + d
        poly              n params: General polynomial: c0 + c1*x + c2*x**2 + ... + cn*x**n
        sabx              2 params: sqrt(f1x), i.e. general sqrt(1/x) function: sqrt(a + b/x)
        see               3 params: Sequential Elementary Effects fitting function: a*(x-b)**c

    Current optimisation test functions are
    ackley                >=2 params:     Ackley function, global optimum: 0.0 at origin
    goldstein_price       2 params:       Goldstein-Price function, global optimum: 3.0 (0.0,-1.0)
    griewank              2 or 10 params: Griewank function, global optimum: 0 at origin
    rastrigin             2 params:       Rastrigin function, global optimum: -2 (0,0)
    rosenbrock            2 params:       Rosenbrock function, global optimum: 0 (1,1)
    six_hump_camelback    2 params:       Six-hump Camelback function
                                          True Optima: -1.031628453489877, (-0.08983,0.7126), (0.08983,-0.7126)

    Current sensitivity analysis test functions are
    saltelli              Example on page 111 of Saltelli et al. (2008)
    Gstar                 G* of Saltelli et al. (2010)
    B                     B  of Saltelli et al. (2010)
    K                     K  of Saltelli et al. (2010)


    Input / Output
    --------------
    See the help of the individual functions for explanations of in/out, etc.


    Examples
    --------
    >>> Rref = 1.0
    >>> E0   = 126.
    >>> T    = 293.15
    >>> resp = 2.0
    >>> from ufz.autostring import astr
    >>> print(astr(lloyd_fix(T, Rref, E0),3,pp=True))
    1.406
    >>> print(astr(lloyd_fix_p(T, [Rref, E0]),3,pp=True))
    1.406
    >>> print(astr(cost_lloyd_fix([Rref, E0], T, resp),3,pp=True))
    0.594
    >>> print(astr(cost2_lloyd_fix([Rref, E0], T, resp),3,pp=True))
    0.353

    >>> print(astr(poly(T,2,1),3,pp=True))
    295.150
    >>> print(astr(poly_p(T,[2,1]),3,pp=True))
    295.150

    >>> print(astr(griewank([0,0]),3,pp=True))
    0.000
    >>> print(astr(goldstein_price([0,-1]),3,pp=True))
    3.000


    License
    -------
    This file is part of the UFZ Python package.

    The UFZ Python package is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    The UFZ Python package is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with the UFZ makefile project (cf. gpl.txt and lgpl.txt).
    If not, see <http://www.gnu.org/licenses/>.

    Copyright 2012-2015 Matthias Cuntz


    History
    -------
    Written,  MC, Oct 2014
    Modified, MC, Mar 2015 - group functions in files
"""
from .opti_test_functions import ackley, griewank, goldstein_price
from .opti_test_functions import rastrigin, rosenbrock, six_hump_camelback
from .sa_test_functions   import B, g, Gstar, K, morris, oakley_ohagan, saltelli
from .fit_functions       import cost_abs, cost_square
from .fit_functions       import arrhenius, arrhenius_p, cost_arrhenius, cost2_arrhenius
from .fit_functions       import f1x, f1x_p, cost_f1x, cost2_f1x
from .fit_functions       import fexp, fexp_p, cost_fexp, cost2_fexp
from .fit_functions       import gauss, gauss_p, cost_gauss, cost2_gauss
from .fit_functions       import lasslop, lasslop_p, cost_lasslop, cost2_lasslop
from .fit_functions       import line, line_p, cost_line, cost2_line
from .fit_functions       import line0, line0_p, cost_line0, cost2_line0
from .fit_functions       import lloyd_fix, lloyd_fix_p, cost_lloyd_fix, cost2_lloyd_fix
from .fit_functions       import lloyd_only_rref, lloyd_only_rref_p, cost_lloyd_only_rref, cost2_lloyd_only_rref
from .fit_functions       import multiline_p
from .fit_functions       import sabx, sabx_p, cost_sabx, cost2_sabx
from .fit_functions       import poly, poly_p, cost_poly, cost2_poly
from .fit_functions       import logistic, logistic_p, cost_logistic, cost2_logistic
from .fit_functions       import logistic_offset, logistic_offset_p, cost_logistic_offset, cost2_logistic_offset
from .fit_functions       import see, see_p, cost_see, cost2_see

# Information
__author__   = "Matthias Cuntz"
__version__  = '1.1'
__revision__ = "Revision: 2071"
__date__     = 'Date: 25.03.2015'
