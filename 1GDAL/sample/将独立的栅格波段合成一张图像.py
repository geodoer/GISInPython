# coding:utf8
# 将独立的栅格波段合成一张图像 - 以tif格式为例
import os
from osgeo import gdal

# 设置工作文件夹
os.chdir(r'D:\osgeopy-2001\Landsat\Washington')
# 三个波段的影像
band1_fn = 'p047r027_7t20000730_z10_nn10.tif'
band2_fn = 'p047r027_7t20000730_z10_nn20.tif'
band3_fn = 'p047r027_7t20000730_z10_nn30.tif'


in_ds = gdal.Open(band1_fn) #打开TIF的影像
in_band = in_ds.GetRasterBand(1) #打开GeoTIFF的波段1

# 创建具有三个波段的GeoTIFF文件（以原文件的属性）
gtiff_driver = gdal.GetDriverByName('GTiff') # 得到GeoTIFF的驱动
out_ds = gtiff_driver.Create('nat_color.tif', # 创建一个新的GeoTIFF文件
    in_band.XSize,
    in_band.YSize,
    3,
    in_band.DataType
)
out_ds.SetProjection(in_ds.GetProjection()) #设置投影
out_ds.SetGeoTransform(in_ds.GetGeoTransform())

# 波段3 - 把前面打开的in_band复制到波段3
in_data = in_band.ReadAsArray()
out_band = out_ds.GetRasterBand(3)
out_band.WriteArray(in_data)

# 波段2 - 将band2_fn复制到波段2
in_ds = gdal.Open(band2_fn)
out_band = out_ds.GetRasterBand(2)
out_band.WriteArray(in_ds.ReadAsArray())

# 波段1 - 将band3_fn复制到波段1
out_ds.GetRasterBand(1).WriteArray(
    gdal.Open(band3_fn).ReadAsArray()
)

# 为每个波段计算统计值
out_ds.FlushCache()
for i in range(1, 4):
    out_ds.GetRasterBand(i).ComputeStatistics(False)

# 创建金字塔图层（概视图）
out_ds.BuildOverviews('average', [2, 4, 8, 16, 32])

del out_ds
