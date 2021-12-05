import arcpy
import os
from arcpy import env
from arcpy.sa import *

arcpy.CheckOutExtension("Spatial")
arcpy.CheckOutExtension("3D")
arcpy.CheckOutExtension("Management")
arcpy.env.overwriteOutput= True

clip_in=r"F:\weiqi_gis_F\tracts\US_tract_2010.shp"
clip_out=r"F:\weiqi_gis_F\output\clip"
env.workspace=r"F:\weiqi_gis_F\States_boundaries"
states_boundaries=arcpy.ListFeatureClasses()
for state_boundary in states_boundaries:
    clip_shape=r"F:\weiqi_gis_F\States_boundaries\{}\{}.shp".format(state_boundary)
    clip_out=os.path.join(clip_out, "{}.shp".format(state_boundary) )
    arcpy.Clip_analysis(in_features=clip_in, clip_features=clip_shape, out_feature_class=clip_out)

for root, dirs, files in os.walk(clip_dir):
    # 遍历文件
    for file in files:
        if file.endswith(".shp"): # 是shp文件
            clip_fp = os.path.join(root, file) #裁剪文件
            out_fp = os.path.join(out_dir, file) #输出文件
            arcpy.Clip_analysis(in_features=in_fp, clip_features=clip_fp, out_feature_class=out_fp)
