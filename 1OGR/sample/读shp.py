# coding:utf8
import sys,os
from osgeo import ogr

inshp_path = r'..\..\92001\park_point_shp\xiamen_20181128_park.shp'

""" 读shp
# 主要步骤
1. 打开shapefile文件，并确保该操作的结果不为空
2. 从数据源中取回第一个图层
3. 查询要素
4. 删除数据源，强制关闭文件
"""


if __name__ == '__main__':
    # （1）打开shapefile文件
    driver = ogr.GetDriverByName('ESRI Shapefile') #【驱动】查找一个特定的驱动程序，名字一定要正确
    datasource = driver.Open(inshp_path, 0) #【数据源】0只读，1可写
    if datasource is None:
        sys.exit('不能够打开{0}'.format(inshp_path))
    # （2）取出图层
    layer = datasource.GetLayer(0) #【图层】得到第一个图层，shp文件只有一个图层
    # （3）查询
    # #########【遍历图层中的要素，并输出指定属性】
    for feature in layer:
        point = feature.geometry()
        x = point.GetX(); y = point.GetY()
        name = feature.GetField('name')
        address = feature.GetField('address')
        print "x={0} y={1} name={2} address={3}".format(x, y, name, address)
    # #########【遍历图层中所有要素并输出其所有属性】
    layer.ResetReading() # 这句话不能少！重置指针
    feature = layer.GetNextFeature()
    while feature:
        feature = layer.GetNextFeature()

    # （4）删除数据源
    del datasource
