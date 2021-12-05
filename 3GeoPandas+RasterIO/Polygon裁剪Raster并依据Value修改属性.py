# -*- coding: utf-8 -*-

# Python中使用面状矢量裁剪栅格影像，并依据Value值更改矢量属性
# https://www.cnblogs.com/MatthewHome/p/10057770.html

from geopandas import *;
import rasterio as rio;
import rasterio.mask;
 
# 读入矢量和栅格文件
shpdatafile='D:/PythonConda/Data/ShpData.shp'
rasterfile='D:/PythonConda/Data/Raster.tif'
out_file='D:/PythonConda/Data/OutShpData'
shpdata=GeoDataFrame.from_file(shpdatafile)
rasterdata=rio.open(rasterfile)
 
out_shpdata = shpdata.copy()
#投影变换，使矢量数据与栅格数据投影参数一致
shpdata=shpdata.to_crs(rasterdata.crs)
 
for i in range(0, len(shpdata)):
    # 获取矢量数据的features
    geo = shpdata.geometry[i]
    feature = [geo.__geo_interface__]
    #通过feature裁剪栅格影像
    out_image, out_transform = rio.mask.mask(rasterdata, feature, all_touched=True, crop=True, nodata=rasterdata.nodata)
    #获取影像Value值，并转化为list
    out_list = out_image.data.tolist()
    #除去list中的Nodata值
    out_list = out_list[0]
    out_data = []
    for k in range(len(out_list)):
        for j in range(len(out_list[k])):
            if out_list[k][j] >=0:
                out_data.append(out_list[k][j])
    #求数据中的众数
    if len(out_data):
        counts = np.bincount(out_data)
        new_type = np.argmax(counts)
    else:
        new_type = None
    #依据众数值更改feature的NewTYPE属性值
    out_shpdata.NewTYPE[i] = new_type
 
#将属性更改过的GeodataFrame导出为shp文件
out_shpdata.to_file(out_file)