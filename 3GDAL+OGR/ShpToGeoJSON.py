# -*- coding: utf-8 -*-
# @Time    : 2019/12/26 15:47
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : ShpToGeoJSON
# @Software: PyCharm
# @Version :
# @Desc    :

from osgeo import ogr
import gdal
import sys
import os

# dict
#   key : shp文件
#   value : json文件
datas = {
    r"D:\LandValue\data\2019.shp" : r"D:\LandValue\data\2019.json",
    r"D:\LandValue\data\SelectPoylgon.shp" : r"D:\LandValue\data\SelectPolygon.json"
}

def ChangeToJson(vector, output):
    print("Starting........")
    #打开矢量图层
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES") #支持文件名称及路径内的中文
    gdal.SetConfigOption("SHAPE_ENCODING", "GBK")        #支持属性字段中的中文
    shp_ds = ogr.Open(vector)
    shp_lyr = shp_ds.GetLayer(0)

    # 创建结果Geojson
    baseName = os.path.basename(output)
    out_driver = ogr.GetDriverByName('GeoJSON')
    out_ds = out_driver.CreateDataSource(output)
    if out_ds.GetLayer(baseName):
        out_ds.DeleteLayer(baseName)
    out_lyr = out_ds.CreateLayer(baseName, shp_lyr.GetSpatialRef())
    out_lyr.CreateFields(shp_lyr.schema)
    out_feat = ogr.Feature(out_lyr.GetLayerDefn())

    #生成结果文件
    for feature in shp_lyr:
        out_feat.SetGeometry(feature.geometry())
        for j in range(feature.GetFieldCount()):
            out_feat.SetField(j, feature.GetField(j))
        out_lyr.CreateFeature(out_feat)

    del out_ds
    del shp_ds
    print("Success........")

def GeoJSONToShp(vector, output):
    print("Starting........")
    # 打开矢量图层
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")  # 支持文件名称及路径内的中文
    gdal.SetConfigOption("SHAPE_ENCODING", "GBK")  # 支持属性字段中的中文
    shp_ds = ogr.Open(vector)
    shp_lyr = shp_ds.GetLayer(0)

    # 创建结果shp
    baseName = os.path.basename(output)
    out_driver = ogr.GetDriverByName('ESRI ShapeFile')
    out_ds = out_driver.CreateDataSource(output)
    if out_ds.GetLayer(baseName):
        out_ds.DeleteLayer(baseName)
    out_lyr = out_ds.CreateLayer(baseName, shp_lyr.GetSpatialRef())
    out_lyr.CreateFields(shp_lyr.schema)
    out_feat = ogr.Feature(out_lyr.GetLayerDefn())

    # 生成结果文件
    for feature in shp_lyr:
        out_feat.SetGeometry(feature.geometry())
        for j in range(feature.GetFieldCount()):
            out_feat.SetField(j, feature.GetField(j))
        out_lyr.CreateFeature(out_feat)

    del out_ds
    del shp_ds
    print("Success........")

if __name__ == '__main__':
    # for key,value in datas.items():
    #     ChangeToJson(key , value)

    ChangeToJson(r"D:\mycode\PythonGIS\workspace\data\2019.shp", r"D:\mycode\PythonGIS\workspace\data\2019.json")
    # ChangeToJson(r"D:\mycode\PythonGIS\workspace\data\SelectPoylgon.shp", r"D:\mycode\PythonGIS\workspace\data\SelectPoylgon.json")

    # GeoJSONToShp(r"D:\mycode\PythonGIS\workspace\data\2019.json", r"D:\mycode\PythonGIS\workspace\data\2019.shp")