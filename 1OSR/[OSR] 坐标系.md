[toc]

【背景】空间参考系统由坐标系、基准面和投影3个部分组成，它们一起影响着一组坐标值
1. 基准面：简单的来说，基准面用来表示地球的曲率
2. 投影：将坐标从一个三维球体转换到二维地图上

【相关名词】

1. 基准：地球表面的非规则形态，导致地球的椭圆体有多种模型，这些模型被称为基准
2. 动态投影：许多地理信息系统在显示不同坐标系的数据时，会将这些数据的坐标系统一，以保证这些数据可以正常显示
3. 空间参考系统：SRS，Spatial Reference System


# OSR

【OSR】osgeo包中包含一个叫作OSR（OGR Spatial Reference，OGR空间参考）的模块，用来处理SRS(空间参考系统)

1. 空间参考系统标识符（SRIDs）：OGC标准中的参数SRID，在地里信息系统中，用来唯一标识每个空间参考系统、基准和其他一些相关信息
2. EPSG：欧洲石油勘测团体（European Petroleum Survey Group）所定义的一大批空间参考，每个空间参考都有一个唯一的ID，它代表特定的椭球体、单位、地理坐标系或投影坐标系等信息。可以在www.spatialreference.org查看代码
3. wkid：WKID的英文全称是Well Known ID，即众所周知的编号。这个编号是大家坐下来一起讨论、约定和认同的，具体有唯一性。arcgis所认同的坐标系id code

## 常量
1. WGS84坐标系的wkt：`osr.SRS_WKT_WGS84`

## 读

### 获取SRS
【异常】如果图层或几何对象不具有SRS信息，两个函数返回None
1. `layer.GetSpatialRef()`
2. `layer.GetSpatial-Reference()`

### 读SRS的具体属性值
【说明】SRIDs、EPSG都是在WKT例子中的AUTHORITY条目

1. `srs.IsGeographic() 或 srs.IsProjected()`：该坐标系是否已经投影 
2. `srs.GetAttrValue('AUTHORITY')`
3. `srs.GetAttrValue('AUTHORITY', 1)`：AUTHORITY在SRS是彼此嵌套的，这个是最少嵌套的，因此它是函数返回的第一个
3. `srs.GetAttrValue('PROJCS')`：异常范围None
4. `srs.GetAuthorityCode('DATUM')`
5. `srs.GetProjParm(osr.SRS_PP_FALSE_EASTING)`

## 创建
### 使用现有坐标系创建
```python
# 【方法一】使用标准EPSG代码，返回0表示成功。可以在www.spatialreference.org查看代码
srs.ImportFromEPSG(26912)

# 【方法二】使用proj.4字符串
srs.ImportFromProj4("+proj=utm +zone=12 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs")

# 【方法三】使用wkt字符串创建
wkt = '''
GEOGCS["GCS_North_American_1983" ,
	DATUM["North_American_Datum_1983",
		SPHEROID["GRS_1980", 6378137.0, 298.25722101],
	],
	PRIMEM["Greenwich", 0.0],
	UNIT["Degree", 0.0174532925199433]
"]
'''
srs = osr.SpatialReference(wkt)
```

【例子】
```python
from osgeo import osr
srs = osr.SpatialReference()
srs.ImportFromEPSG(26912) #按照EPSG创建
srs.GetAttrValue('PROJCS')
```

### 自定义坐标系
【参数依次包括】
1. 标准平行线
2. 中央纬线
3. 中央经线
4. 东移假定值
5. 北移假定值

【例子】
```python
srs = osr.SpatialReference()
srs.SetProjCS('USGS Albers') #设置名称
srs.SetWellKnwonGeogCS('NAD83') #指定基准或椭球体
srs.SetACEA(29.5, 45.5, 23, -96, 0, 0) # 为Albers投影提供所需的参数
srs.Fixup() #为缺少的参数添加默认值，并重新排序项目，以使它们与标准匹配
srs.Validate() #验证：返回0表示一切正常
```

## 为数据分配SRS
【注意】这里是为一个数据集添加一个注释，注明这个数据的SRS。而并不是将该数据集转坐标系，如果需要重新投影，请看下节

```python
# 【case】创建一个shp时，SRS作为第二个参数传入
lyr = datasource.CreateLayer("sounties", srs, ogr.wkbPolygon)
# 【case】为geometry注释他的坐标系
geometry.AssignSpatialReference(srs)
```

## 为Geometry重投影
### Geometry里有坐标系信息

```python
# 【例子】UTM转Web墨卡托
from osgeo import gdal
gdal.SetConfigOption('OGR_ENABLE_PARTIAL_REPROJECTION', 'TRUE')
	# 【注意】某些点（比如北极和南极）不能总是被成功地重投影。因此还需要使用内置模块来设置环境变量，告诉它可以跳过这些点
web_mercator_srs = osr.SpatialReference()
web_mercator_srs.ImportFromEPSG(3857) #创建Web墨卡托
geometry.TransformTo(web_mercator_srs) #转换坐标
```

### Geometry里没有坐标系信息
```python
# 【背景】Geometry中虽然没有坐标信息，但我们知道它的坐标系是Web墨卡托
# 【例子】将Geometry转换为Gall-Peters投影
peters_srs = osr.SpatialReference()
peters_srs.ImportFromProj4("+proj=cea +lon_0=0 +x_0=0 +y_0=0 +lat_ts=45 +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
ct = osr.CoordinateTransformation(web_mercator_srs, peters_sr) #定义一个坐标转换对象
geometry.Transform(ct) # 按照这个坐标转换对象来进行重定义
```

## 为整个图层重投影
【说明】没有函数可以一次投影整个图层，所以需要遍历feature进行投影

```python
# coding:utf8

from osgeo import ogr, osr

# 创建一个坐标系
sr = osr.SpatialReference()
sr.ImportFromProj4('''+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23
                      +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80
                      +datum=NAD83 +units=m +no_defs''')

# 在指定文件夹中打开一个datasource
ds = ogr.Open(2001, 1)

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
```