# coding:utf8

from osgeo import ogr, osr

# 创建一个坐标系
sr = osr.SpatialReference()
sr.ImportFromProj4('''+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23
                      +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80
                      +datum=NAD83 +units=m +no_defs''')

# 在指定文件夹中打开一个datasource
ds = ogr.Open(r'D:\osgeopy-2001\US', 1)

# 得到目标图层
in_lyr = ds.GetLayer('us_volcanos')

# 创建一个新的输出图层
out_lyr = ds.CreateLayer('us_volcanos_aea', sr, ogr.wkbPoint)
out_lyr.CreateFields(in_lyr.schema)

# 遍历图层中的feature
out_feat = ogr.Feature(out_lyr.GetLayerDefn()) #创建一个空的feature
for in_feat in in_lyr:
    # 复制geometry，然后转换坐标系
    geom = in_feat.geometry().Clone()
    geom.TransformTo(sr)
    out_feat.SetGeometry(geom)

    # 复制属性
    for i in range(in_feat.GetFieldCount()):
        out_feat.SetField(i, in_feat.GetField(i))

    # 插入到新图层中
    out_lyr.CreateFeature(out_feat)
