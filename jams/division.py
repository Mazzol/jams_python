#!/usr/bin/env python
from __future__ import division, absolute_import, print_function
import numpy as np

def division(a, b, otherwise=np.nan, prec=0.):
    """
        Divide two arrays, return "otherwise" if division by 0.


        Definition
        ----------
        def division(a, b, otherwise=np.nan, prec=0.):
          There is a wrapper function for convenience with the short name 'div'.


        Input
        -----
        a            enumerator
        b            denominator


        Optional Input
        --------------
        otherwise    value to return if b=0 (default: np.nan)
        prec         if |b|<|prec| then otherwise


        Output
        ------
        a/b          if |b|>|prec|
        otherwise    if |b|<=|prec|


        Restrictions
        ------------
        None.


        Examples
        --------
        >>> from autostring import astr
        >>> print(astr(division([1., 2., 3.], 2.),1,pp=True))
        ['0.5' '1.0' '1.5']

        >>> print(astr(division([1., 1., 1.], [2., 1., 0.]),1,pp=True))
        ['0.5' '1.0' 'nan']

        >>> print(astr(division([1., 1., 1.], [2., 1., 0.], 0.),1,pp=True))
        ['0.5' '1.0' '0.0']

        >>> print(astr(division([1., 1., 1.], [2., 1., 0.], otherwise=0.),1,pp=True))
        ['0.5' '1.0' '0.0']

        >>> print(astr(division([1., 1., 1.], [2., 1., 0.], prec=1.),1,pp=True))
        ['0.5' 'nan' 'nan']


        License
        -------
        This file is part of the JAMS Python package, distributed under the MIT
        License. The JAMS Python package originates from the former UFZ Python library,
        Department of Computational Hydrosystems, Helmholtz Centre for Environmental
        Research - UFZ, Leipzig, Germany.

        Copyright (c) 2012-2015 Matthias Cuntz - mc (at) macu (dot) de

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.


        History
        -------
        Written,  MC, Jan 2012
        Modified, MC, May 2012 - div
                  MC, Feb 2013 - ported to Python 3
                  MC, Oct 2014 - do not return masked array if no masked array given
                  MC, Sep 2015 - bug: returned non-masked array in case of masked array input
    """
    oldsettings = np.geterr()
    np.seterr(divide='ignore')

    if isinstance(a, np.ma.masked_array) or isinstance(b, np.ma.masked_array):
        out = np.ma.where(np.ma.abs(np.ma.array(b)) > np.abs(prec), np.ma.array(a)/np.ma.array(b), otherwise)
    else:
        out = np.where(np.abs(np.array(b)) > np.abs(prec), np.array(a)/np.array(b), otherwise)

    np.seterr(**oldsettings)

    return out



def div(*args, **kwargs):
    """
        Wrapper function for division
        def division(a, b, otherwise=np.nan, prec=0.):


        Examples
        --------
        >>> from autostring import astr
        >>> print(astr(div([1., 2., 3.], 2.),1,pp=True))
        ['0.5' '1.0' '1.5']

        >>> print(astr(div([1., 1., 1.], [2., 1., 0.]),1,pp=True))
        ['0.5' '1.0' 'nan']

        >>> print(astr(div([1., 1., 1.], [2., 1., 0.], 0.),1,pp=True))
        ['0.5' '1.0' '0.0']

        >>> print(astr(div([1., 1., 1.], [2., 1., 0.], otherwise=0.),1,pp=True))
        ['0.5' '1.0' '0.0']

        >>> print(astr(div([1., 1., 1.], [2., 1., 0.], prec=1.),1,pp=True))
        ['0.5' 'nan' 'nan']
    """
    return division(*args, **kwargs)


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)

