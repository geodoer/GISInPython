# -*- coding: utf-8 -*-
# @Time    : 2019/6/5 10:53
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    :
# @Software: PyCharm
# @Version :
# @Desc    : 【批量】提取栅格外框线，并裁剪

import arcpy
import os
from arcpy import env
from arcpy.sa import *

arcpy.CheckOutExtension("Spatial")
arcpy.CheckOutExtension("3D")
arcpy.CheckOutExtension("Management")
arcpy.env.overwriteOutput= True

gdb_path = r'D:\mycode\GISandPython\2Arcpy\data\txt.gdb' #gdb文件夹：栅格路径
out_dir = r'D:\mycode\GISandPython\2Arcpy\data\output' #输出文件夹
clip_shp = r'D:\mycode\GISandPython\2Arcpy\data\clip_shp\clip.shp' #裁剪的文件：美国省界图

# gdb_path = arcpy.GetParameterAsText(0)
# out_dir = arcpy.GetParameterAsText(1)
# clip_shp = arcpy.GetParameterAsText(2)


# 创建文件夹
arcpy.CreateFileGDB_management(out_dir, "reclass.gdb")
reclass_dir = os.path.join(out_dir, "reclass.gdb")

polygon_dir = os.path.join(out_dir, "polygon_dir")
clip_dir = os.path.join(out_dir, "clip")
if os.path.exists(polygon_dir) is False:
    os.mkdir(polygon_dir)
if os.path.exists(clip_dir) is False:
    os.mkdir(clip_dir)


# 重分类
print "======= reclassify ======="
env.workspace = gdb_path #设置工程环境
rasters = arcpy.ListRasters()
for raster in rasters:
    fin = os.path.join(gdb_path, raster)
    fout = os.path.join(reclass_dir, raster )

    print "[doing] {}".format(fin)
    # 重分类
    myRemapRange = RemapRange([ [-100, 100, 1]] )
    outReclass = Reclassify(fin, "VALUE", myRemapRange)
    outReclass.save(fout)
    print "[done] {}".format( fout )

# 转shp
print "======= to shp ======="
env.workspace = reclass_dir
for raster in rasters:
    fin = os.path.join(reclass_dir, raster)
    fout = os.path.join(polygon_dir, "{}.shp".format(raster) )

    print "[doing] {}".format(fin)
    arcpy.RasterToPolygon_conversion(raster,
        fout,
        "NO_SIMPLIFY",
        "VALUE"
    )
    print "[done] {}".format(fout)

# 裁剪
print "======= clip ======="
env.workspace = polygon_dir
for shp_name in arcpy.ListFeatureClasses():
    fin = os.path.join(polygon_dir, shp_name)
    fout = os.path.join(clip_dir, shp_name)

    print "[doing] {}".format(fin)
    arcpy.Clip_analysis(in_features=fin, clip_features=clip_shp, out_feature_class=fout)
    print "[done] {}".format(fout)