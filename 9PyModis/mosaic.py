# -*- coding: utf-8 -*-
# @Time    : 2019/8/2 22:05
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : mosaic
# @Software: PyCharm
# @Version :
# @Desc    :
import os
import glob
from pymodis.convertmodis_gdal import createMosaicGDAL

in_dir = r"D:\mycode\GISandPython\2PyModis\2001"
in_files = glob.glob( in_dir + "\*.hdf")
print(in_files)

output_pref = r"D:\mycode\GISandPython\2PyModis\tmp\mosic"
output_tif = r"D:\mycode\GISandPython\2PyModis\tmp\mosic.tif"


subset = [0 for x in range(0, 219) ]
subset[11] = 1

mosaic = createMosaicGDAL(in_files, subset, 'GTiff')
mosaic.run(output_tif)
# mosaic.write_vrt(output_pref)