# coding:utf8
# Use a flawed method to find out how many US cities are within 16,000
# meters of a volcano.

from osgeo import ogr

shp_ds = ogr.Open(r'D:\osgeopy-2001\US')
volcano_lyr = shp_ds.GetLayer('us_volcanos_albers')
cities_lyr = shp_ds.GetLayer('cities_albers')

# 创建一个临时图层，用于存储缓冲区域
memory_driver = ogr.GetDriverByName('memory')
memory_ds = memory_driver.CreateDataSource('temp')
buff_lyr = memory_ds.CreateLayer('buffer')
buff_feat = ogr.Feature(buff_lyr.GetLayerDefn())

# 缓冲每一个火山点，将结果添加到缓冲图层中
for volcano_feat in volcano_lyr:
    buff_geom = volcano_feat.geometry().Buffer(16000)
    tmp = buff_feat.SetGeometry(buff_geom)
    tmp = buff_lyr.CreateFeature(buff_feat)


# 将城市图层与火山缓冲图层相交
result_lyr = memory_ds.CreateLayer('result')
buff_lyr.Intersection(cities_lyr, result_lyr)

# 获得城市数：美国有多少个城市在火山1600米范围内
print('Cities: {}'.format(result_lyr.GetFeatureCount()))
