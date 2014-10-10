#!/usr/bin/env python
from __future__ import print_function
import numpy as np

def alpha_kin_h2o(isotope=None, eps=False, greater1=True, boundary=False, cappa=False):
    """
        Calculates the kinetic fractionation factors for molecular diffusion of water isotoploques.
        It does not use the atmospheric convention, i.e. factor<1, but defaults to >1 (greater1=True).


        Definition
        ----------
        def alpha_kin_h2o(isotope=None, eps=False, greater1=True, boundary=False, cappa=False):


        Optional Input
        --------------
        isotope    which water isotopologue: 1: HDO; 2: H218O; else: no fractionation, return 1 (default)
        eps        reports epsilon=alpha-1 instead of alpha
        greater1   not atmospheric convention, i.e. alpha > 1 (default)
        boundary   reports alpha^2/3 for diffusion through boundary layer
        cappa      uses factors of Cappa et al. (2003) instead of Merlivat (1978)


        Output
        ------
        Kinetic fractionation factors


        Restrictions
        ------------
        None


        Literature
        ----------
        Cappa, C. D., Hendricks, M. B., DePaolo, D. J., & Cohen, R. (2003)
            Isotopic fractionation of water during evaporation
            Journal of Geophysical Research, 108(D16), 4525. doi:10.1029/2003JD003597
        Merlivat, L. (1978)
            Molecular Diffusivities Of (H2O)-O-16 HD16O, And (H2O)-O-18 In Gases
            The Journal of Chemical Physics, 69(6), 2864-2871.
        Merlivat, L., & Jouzel, J. (1979)
            Global climatic interpretation of the deuterium-oxygen-18 relationship for precipitation
            Journal of Geophysical Research, 84(C8), 5029-5033.


        Examples
        --------
        >>> from autostring import astr
        >>> print(astr(alpha_kin_h2o(isotope=0), 4))
        1.0000
    
        >>> print(astr(alpha_kin_h2o(isotope=1, eps=True)*1000., 4))
        25.1153

        >>> print(astr(alpha_kin_h2o(isotope=2, eps=True, greater1=False)*1000., 4))
        -27.3000

        >>> print(astr(alpha_kin_h2o(isotope=2, eps=True, greater1=True, boundary=True)*1000., 4))
        18.6244

        >>> print(astr(alpha_kin_h2o(isotope=2, eps=True, greater1=False, boundary=True, cappa=True)*1000., 4))
        -20.7076


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

        Copyright 2014 Matthias Cuntz


        History
        -------
        Written,  MC, Sep 2014
    """
    # Fractionation factors
    if (isotope==1): # HDO
        if cappa:
            out = 0.9839
        else:
            out = 0.9755
    elif (isotope==2): # H218O
        if cappa:
            out = 0.9691
        else:
            out = 0.9727
    else:
        out = 1.

    # boundary layer
    if boundary:
        out = out**(2./3.)

    # alpha+
    if greater1:
        out = 1./out

    # epsilon
    if eps:
        out -= 1.

    return out


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)

    # from autostring import astr
    # print(astr(alpha_kin_h2o(isotope=0), 4))
    # # 1.0000
    
    # print(astr(alpha_kin_h2o(isotope=1, eps=True)*1000., 4))
    # # 25.1153

    # print(astr(alpha_kin_h2o(isotope=2, eps=True, greater1=False)*1000., 4))
    # # -27.3000

    # print(astr(alpha_kin_h2o(isotope=2, eps=True, greater1=True, boundary=True)*1000., 4))
    # # 18.6244

    # print(astr(alpha_kin_h2o(isotope=2, eps=True, greater1=False, boundary=True, cappa=True)*1000., 4))
    # # -20.7076