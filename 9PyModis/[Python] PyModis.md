

# 前言

## 介绍

【NASA官网】

1. [用户注册](https://urs.earthdata.nasa.gov/users/new)
2. [手动下载少量MODIS数据](https://search.earthdata.nasa.gov/search?m=0!0.0703125!2!1!0!0%2C2&q=MCD43D22%20V006)

【PyModis官网】http://www.pymodis.org/

【PyModis简介】基于Python的开源Modis数据处理库

1. 下载功能：根据用户提供时间批量下载
2. 读取：提取数据元数据（包含数据质量信息）
3. 处理：镶嵌、投影、转格式

【官方介绍】

1. 下载大量modis hdf/xml 文件以及解析xml文档以获取有关HDF文件的信息
2. 使用MRT或GDAL将modis文件转为geotiff格式
3. 使用MRT或GDAL将modis瓦片数据拼接、重投影
4. 用于下载大量modis hdf/xml 文件以及解析xml文档以获取有关HDF文件的信息
5. 创建融合后影像的xml格式元数据
6. 从modis字节编码质量评估图层提取具体信息

## 使用方法

【两种使用方法】

1. 脚本工具（.py）：命令行调用
2. Pymodis库：Python代码调用

## 安装

【PyModis安装】

1. PyModis依赖于GDAL库：[安装GDAL](https://blog.csdn.net/summer_dew/article/details/86600257#PythonGDAL_35)
2. 安装PyModis：`pip install pymodis`



# PyModis库使用

【预处理】

1. createMosaicGDAL实现拼接
2. convertModisGDAL将hdf波段导出为TIFF，并可对TIFF重采样、投影变化等

## downmodis

### 参数说明

【官方说明】

```
url         下载地址 [默认=https://e4ftl01.cr.usgs.gov]
password	密码
user		用户名
tiles		要下载产品的行列号
			  [格式] 用逗号隔开 或 数组形式
              [default=none] 下载所有
              [示例] "h18v03,h18v04"
              [解释] 下载 18行3列 和 18行4列的数据瓦片
path		url与产品目录之间的路径
product     产品名称 
			  [默认=MOD11A1.005]
delta       从下载日期开始，往前下载多少天 
			  [默认=10]
today    	开始时间 
			  [格式]YYYY-MM-DD
              [默认=none] 默认为今天
enddate     结束日期（应该比today早，因为它是从today往前下载的）
			  [说明]如果delta与enddate都有设置，以enddate为主
jpg			是否下载jpg数据
```



### 示例



## convertmodis_gdal

### 参数说明

【hdfname】输入的hdf文件路径

【prefix】输出文件的名字前缀，程序会在后面自动加上一个波段名字

```python
prefix = r"D:\mycode\GISandPython\2PyModis\tmp\out"
# 输出的文件名字为：
# D:\mycode\GISandPython\2PyModis\tmp\out_Image_Optical_Depth_Land_And_Ocean.tif
# 其中，Image_Optical_Depth_Land_And_Ocean为第11波段的名字，为程序自动添加的
```

【subset】处理的波段

```python
# 【方法1】下标对应为1，则为要处理的波段
subset = [0 for x in range(0, 219) ]  #生成219个0的数组
subset[11] = 1						  #处理第11个波段
subset[14] = 1						  #处理第14个波段
```

【res】分辨率，单位即为坐标系的单位

【outformat】输出的格式（GDAL库中的格式）

1. `GTiff`：TIFF

【epsg】坐标系的EPSG编码，可[查看](http://epsg.io/)

【wkt】坐标系的第二种设置方式：wkt格式的字符串（prj文件）

```python
wkt=r"D:\WGS84.prj" # 投影文件
	# 你可以在ArcGIS里创建一个对应坐标系的shp文件，生成的.prj即可用
```

【resampl】重采样方法

1. NEAREST_NEIGHBOR

【vrt】是否生成影像的头文件（默认为False：不生成）

### 示例

```python
import pymodis

# 处理的波段
subset = [0 for x in range(0, 219) ]
subset[11] = 1 #只处理第11波段
# 转换成TIFF格式
convertmodis = pymodis.convertmodis_gdal.convertModisGDAL(
    hdfname = r"D:\mycode\GISandPython\2PyModis\2001\MOD04_L2.A2001001.0110.061.2017220225602.hdf",
    prefix = r"D:\mycode\GISandPython\2PyModis\tmp\4326",
    subset= subset,
    res=1,              #设置的为WGS84坐标系，那么单位为°，则此为设置为1°
    outformat='GTiff',
    epsg=4326,          #WGS84
    resampl='NEAREST_NEIGHBOR'
)
convertmodis.run()
```

【程序运行结果】

![运行结果](https://img-blog.csdnimg.cn/20190803192735187.png)

【Projection情况】
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190803194647472.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)
【分辨率】1°
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190803194652399.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)
【坐标系】WGS84
![在这里插入图片描述](https://img-blog.csdnimg.cn/2019080319470072.png)



# 相关链接



1. [MODIS数据批量下载与处理](https://blog.csdn.net/qq_40821274/article/details/94739578#_33)
