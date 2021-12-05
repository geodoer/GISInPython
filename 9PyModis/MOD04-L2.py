# -*- coding: utf-8 -*-
# @Time    : 2019/8/2 22:23
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : MOD04-L2
# @Software: PyCharm
# @Version :
# @Desc    :

import pymodis

# 处理的波段
subset = [0 for x in range(0, 219) ]
subset[11] = 1 #只处理第11波段
subset[212] = 1
# 转换成TIFF格式
convertmodis = pymodis.convertmodis_gdal.convertModisGDAL(
    hdfname = r"D:\mycode\GISandPython\2PyModis\2001\MOD04_L2.A2001001.0110.061.2017220225602.hdf",
    prefix = r"D:\mycode\GISandPython\2PyModis\tmp\test",
    subset= subset,
    res=1,
    outformat='GTiff',
    wkt = r"D:\mycode\GISandPython\1.2OSR Proj\prj\WGS84.prj",
    resampl='NEAREST_NEIGHBOR'
)
convertmodis.run()