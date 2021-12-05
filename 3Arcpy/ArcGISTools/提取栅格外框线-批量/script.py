import arcpy
import os
from arcpy import env
from arcpy.sa import *

arcpy.CheckOutExtension("Spatial")
arcpy.CheckOutExtension("3D")
arcpy.CheckOutExtension("Management")
arcpy.env.overwriteOutput= True


gdb_path = arcpy.GetParameterAsText(0)
out_dir = arcpy.GetParameterAsText(1)
clip_shp = arcpy.GetParameterAsText(2)


arcpy.CreateFileGDB_management(out_dir, "reclass.gdb")
reclass_dir = os.path.join(out_dir, "reclass.gdb")

polygon_dir = os.path.join(out_dir, "polygon_dir")
clip_dir = os.path.join(out_dir, "clip")
if os.path.exists(polygon_dir) is False:
    os.mkdir(polygon_dir)
if os.path.exists(clip_dir) is False:
    os.mkdir(clip_dir)

print "======= reclassify ======="
env.workspace = gdb_path
rasters = arcpy.ListRasters()
for raster in rasters:
    fin = os.path.join(gdb_path, raster)
    fout = os.path.join(reclass_dir, raster )

    print "[doing] {}".format(fin)

    myRemapRange = RemapRange([ [-100, 100, 1]] )
    outReclass = Reclassify(fin, "VALUE", myRemapRange)
    outReclass.save(fout)
    print "[done] {}".format( fout )

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

print "======= clip ======="
env.workspace = polygon_dir
for shp_name in arcpy.ListFeatureClasses():
    fin = os.path.join(polygon_dir, shp_name)
    fout = os.path.join(clip_dir, shp_name)

    print "[doing] {}".format(fin)
    arcpy.Clip_analysis(in_features=fin, clip_features=clip_shp, out_feature_class=fout)
    print "[done] {}".format(fout)