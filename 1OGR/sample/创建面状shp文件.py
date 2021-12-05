# coding:utf8
from collections import OrderedDict
from osgeo import ogr
from osgeo import osr
import os,math


# 点坐标
north_west_point = (25.072465, 117.641602)  #左上
north_east_point = (25.072465, 118.526001)  #右上
south_east_point = (24.319286, 118.526001)  #右下
south_west_point = (24.319286, 117.641602)  #左下
# 将许多个点，打包成points。但是一定要注意，点要顺时针
points = [north_west_point, north_east_point, south_east_point, south_west_point] #顺时针


if __name__ == '__main__':
    # 1. 得到shp文件的驱动
    driver = ogr.GetDriverByName("ESRI Shapefile")
    # 2. 得到shp文件存放路径，并查看是否已经存在
    out_file_name = "polygon"
    out_file_path = r"polygon.shp"
    if os.access(out_file_path, os.F_OK):
        # 若存在，删除
        driver.DeleteDataSource( out_file_path )

    # 3. 创建该shp文件
    ds = driver.CreateDataSource(out_file_path) #创建shp文件

    # 4. 创建图层
    # 4.1 创建坐标系
    srs= osr.SpatialReference()
    srs.SetWellKnownGeogCS('WGS84')
    # 4.2 创建图层
    layer = ds.CreateLayer(name=out_file_name,
        srs=srs,
        geom_type=ogr.wkbPolygon,
        options  = [ #设置编码
            "ENCODING=UTF-8"
        ]
    )
    # 4.3 创建图层的字段定义
    fieldcnstr = ogr.FieldDefn("name", ogr.OFTString)  # 创建字段(字段名，类型)
    fieldcnstr.SetWidth(32)  # 设置宽度
    layer.CreateField(fieldcnstr)  # 将字段设置到layer

    # 5. 创建feature
    feat = ogr.Feature(layer.GetLayerDefn()) #按照图层的定义（包含坐标系与字段等），来创建Feature

    # 6. 创建Geometry->并将Geometry给Feature->并将Feature加入图层
    ring = ogr.Geometry(ogr.wkbLinearRing) #创建环
    for point in points:
        ring.AddPoint(point[1], point[0]) #经度，纬度
    polygon = ogr.Geometry(ogr.wkbPolygon) #创建面
    polygon.AddGeometry(ring) # 将环加入面
    polygon.CloseRings() #首尾关闭
    feat.SetGeometry(polygon) # 将Geometry给feature
    feat.SetField('name', "我是字段值")  # 设置字段值
    layer.CreateFeature(feat) #并将Feature加入图层

    # 7. 释放ds，写入shp文件
    ds.Destroy()

