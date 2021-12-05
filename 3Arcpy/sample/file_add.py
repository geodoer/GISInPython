import arcpy
from arcpy import env
from arcpy.sa import *

arcpy.CheckOutExtension("spatial") #检查权限
env.workspace = r"E:\user\Desktop\date" #工作目录

rasters = arcpy.ListRasters("19*", "IMG") #打开要相加的栅格数据集

out = Raster('roi_value_0') #打开值为0的基础文件
for raster in rasters: #遍历栅格文件
    out = Con( (raster > out), raster, out )
out.save(r"E:\user\Desktop\NDVI_result\max_date")