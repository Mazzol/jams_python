#!/usr/bin/env python
from __future__ import division, absolute_import, print_function
import numpy as np

def readhdf4(fName, var='', reform=False, squeeze=False, variables=False,
            attributes=False, fileattributes=False, sort=False):
    """
        Get variables or print information of hdf4 file.


        Definition
        ----------
        def readhdf4(fName, var='', reform=False, squeeze=False, variables=False,
                     attributes=False, fileattributes=False, sort=False):

        Input
        -----
        fName            hdf4 file name


        Optional Input Parameters
        -------------------------
        var              name of variable in hdf4 file


        Options
        -------
        reform           if output is array then squeeze(array)
        squeeze          same as reform
        variables        get list of variables in hdf4 file
        attributes       get dictionary of all attributes of specific variable
        fileattributes   get dictionary of all attributes of the file
        sort             sort variable names


        Output
        ------
        Either variable array or information of file or variable
        such as list of all variables or attributes of a variable.


        Examples
        --------
        >>> var = readhdf4('test_readhdf4.hdf4', fileattributes=True)
        >>> print(list(var.keys()))
        ['OldCoreMetadata.0', 'HDFEOSVersion', 'OldArchiveMetadata.0', 'OldStructMetadata.0', 'StructMetadata.0']
        >>> print(var['HDFEOSVersion'])
        ('HDFEOS_V2.14', 0, 4, 12)

        >>> var = readhdf4('test_readhdf4.hdf4', variables=True)
        >>> print(var)
        ['QC_250m_1', 'sur_refl_b02_1', 'sur_refl_b01_1', 'num_observations']

        >>> var = readhdf4('test_readhdf4.hdf4', variables=True, sort=True)
        >>> print(var)
        ['QC_250m_1', 'num_observations', 'sur_refl_b01_1', 'sur_refl_b02_1']

        >>> var = readhdf4('test_readhdf4.hdf4', var='sur_refl_b01_1')
        >>> print(var)
        [[7492 7327 7327 7131 7187]
         [6604 6604 7423 7131 7131]
         [7441 7441 7423 7423 7507]]

        >>> var = readhdf4('test_readhdf4.hdf4', var='sur_refl_b01_1', attributes=True)
        >>> print(list(var.keys()))
        ['_FillValue', 'Nadir Data Resolution', 'scale_factor', 'valid_range', 'add_offset', 'long_name', 'calibrated_nt', 'units', 'scale_factor_err', 'add_offset_err', 'HorizontalDatumName']
        >>> print(var['_FillValue'])
        (-28672, 3, 22, 1)


        License
        -------
        This file is part of the JAMS Python package, distributed under the MIT
        License. The JAMS Python package originates from the former UFZ Python library,
        Department of Computational Hydrosystems, Helmholtz Centre for Environmental
        Research - UFZ, Leipzig, Germany.

        Copyright (c) 2012-2013 Matthias Cuntz - mc (at) macu (dot) de

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
        Written,  MC, Jun 2012
        Modified, MC, Feb 2013 - ported to Python 3
                  MC, Oct 2013 - hdf4read
    """
    try:
        from pyhdf.SD import SD
    except:
        raise Error('No HDF4 support available, i.e. pyhdf')
    # Open hdf4 file
    try:
        f = SD(fName)
    except HDF4Error:
        raise IOError('Cannot open file: '+fName)
    # Get attributes of the file
    if fileattributes:
        attr = f.attributes(full=1)
        f.end()
        return attr
    # Variables
    svars = list(f.datasets().keys())
    # Sort and get sort indices
    if variables:
      f.end()
      if sort:
        svars.sort()
        return svars
      else:
        return svars
    # Get attributes of variables
    if attributes:
      if var not in svars:
          f.end()
          raise ValueError('Variable '+var+' not in file '+fname)
      attrs = f.select(var).attributes(full=1)
      f.end()
      return attrs
    # Get variable
    if var == '':
        f.end()
        raise ValueError('Variable name has to be given.')
    if var != '':
      if var not in svars:
          f.end()
          raise ValueError('Variable '+var+' not in file '+fname)
 #     try:
      arr = np.array(f.select(var).get())
 #     except ValueError:
 #         f.end()
 #         raise IOError('Cannot read variable '+var+' in file '+fName)
      f.end()
      if reform or squeeze:
        return arr.squeeze()
      else:
        return arr


def hdf4read(*args, **kwargs):
    """
        Wrapper for readhdf4.
        def readhdf4(fName, var='', reform=False, squeeze=False, variables=False,
                     attributes=False, fileattributes=False, sort=False):


        Examples
        --------
        >>> from pyhdf.SD import SD
        >>> var = hdf4read('test_readhdf4.hdf4', fileattributes=True)
        >>> print(list(var.keys()))
        ['OldCoreMetadata.0', 'HDFEOSVersion', 'OldArchiveMetadata.0', 'OldStructMetadata.0', 'StructMetadata.0']
        >>> print(var['HDFEOSVersion'])
        ('HDFEOS_V2.14', 0, 4, 12)

        >>> var = hdf4read('test_readhdf4.hdf4', variables=True)
        >>> print(var)
        ['QC_250m_1', 'sur_refl_b02_1', 'sur_refl_b01_1', 'num_observations']

        >>> var = hdf4read('test_readhdf4.hdf4', variables=True, sort=True)
        >>> print(var)
        ['QC_250m_1', 'num_observations', 'sur_refl_b01_1', 'sur_refl_b02_1']

        >>> var = hdf4read('test_readhdf4.hdf4', var='sur_refl_b01_1')
        >>> print(var)
        [[7492 7327 7327 7131 7187]
         [6604 6604 7423 7131 7131]
         [7441 7441 7423 7423 7507]]

        >>> var = hdf4read('test_readhdf4.hdf4', var='sur_refl_b01_1', attributes=True)
        >>> print(list(var.keys()))
        ['_FillValue', 'Nadir Data Resolution', 'scale_factor', 'valid_range', 'add_offset', 'long_name', 'calibrated_nt', 'units', 'scale_factor_err', 'add_offset_err', 'HorizontalDatumName']
        >>> print(var['_FillValue'])
        (-28672, 3, 22, 1)
    """
    return readhdf4(*args, **kwargs)


if __name__ == '__main__':
    import doctest
    try:
        from pyhdf.SD import SD
    except ImportError:
        raise ImportError('No HDF4 support available, i.e. pyhdf')
    doctest.testmod(optionflags=(doctest.NORMALIZE_WHITESPACE | doctest.IGNORE_EXCEPTION_DETAIL))

    # var = readhdf4('test_readhdf4.hdf4', fileattributes=True)
    # print var.keys()
    # # ['OldCoreMetadata.0',
    # #  'HDFEOSVersion',
    # #  'OldArchiveMetadata.0',
    # #  'OldStructMetadata.0',
    # #  'StructMetadata.0']
    # print var['HDFEOSVersion']
    # # ('HDFEOS_V2.14', 0, 4, 12)

    # var = readhdf4('test_readhdf4.hdf4', variables=True)
    # print var
    # # ['QC_250m_1', 'sur_refl_b02_1', 'sur_refl_b01_1', 'num_observations']

    # var = readhdf4('test_readhdf4.hdf4', variables=True, sort=True)
    # print var
    # # ['QC_250m_1', 'num_observations', 'sur_refl_b01_1', 'sur_refl_b02_1']

    # var = readhdf4('test_readhdf4.hdf4', var='sur_refl_b01_1')
    # print var
    # # [[7492 7327 7327 7131 7187]
    # #  [6604 6604 7423 7131 7131]
    # #  [7441 7441 7423 7423 7507]]

    # var = readhdf4('test_readhdf4.hdf4', var='sur_refl_b01_1', attributes=True)
    # print var.keys()
    # # ['_FillValue',
    # #  'Nadir Data Resolution',
    # #  'scale_factor',
    # #  'valid_range',
    # #  'add_offset',
    # #  'long_name',
    # #  'calibrated_nt',
    # #  'units',
    # #  'scale_factor_err',
    # #  'add_offset_err',
    # #  'HorizontalDatumName']
    # print var['_FillValue']
    # # (-28672, 3, 22, 1)
