# -*- coding: utf-8 -*-
# @Time    : 2019/4/10 11:09
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : __init__
# @Software: PyCharm
# @Version :
# @Desc    :

try:
    from osgeo import gdal
except ImportError:
    import gdal

import sys
from Util.coordinate_conversion import gcj02towgs84_extent


# 文件夹设置
original_dir = r"D:\mycode\GISandPython\1.3 GDAL\1example\图像处理实例\data\original"
registration_dir = r'D:\mycode\GISandPython\1.3 GDAL\1example\图像处理实例\data\registration'
mosaic_dir = r'D:\mycode\GISandPython\1.3 GDAL\1example\图像处理实例\data\mosaic'

if __name__ == '__main__':
    # 读取original_dir中图像的信息
    import os
    import json
    infos_fp = os.path.join(original_dir, "infos.json")
    with open(infos_fp, "r") as f:
        infos = json.load(f)
        f.close()

    # GCJ02转WGS84坐标
    for time,time_value in infos.items():
        extent_gcj02 = time_value["extent_gcj02"]
        extent_wgs84 = gcj02towgs84_extent(extent_gcj02)
        time_value["extent_wgs84"] = extent_wgs84
    print(infos)

    # 将Png转成tif格式
    from PIL import Image # pip install pillow
    for time,time_value in infos.items():
        # 打开png
        png_fn = time_value["file_name"]
        png_fp = os.path.join(original_dir, png_fn)
        im = Image.open(png_fp)
        # 保存成tif
        filename = png_fn.split('.')[0] #文件名，不含文件格式.png
        tif_fn = "{}.tif".format(filename)
        tif_fp = os.path.join(registration_dir, tif_fn)
        im.save(tif_fp)
        time_value["tif_fp"] = tif_fp
    print(infos)

    # 按照四个角点坐标（WGS84）配准
    from osgeo import osr
    subimgs = []
    for time,time_value in infos.items():
        tif_fp = time_value["tif_fp"]
        extent_wgs84 = time_value["extent_wgs84"]

        x1, y1, x2, y2 = extent_wgs84
        # 用extent_wgs84对tif_fp文件进行配准
        ds = gdal.Open(tif_fp, gdal.GA_Update)  # 打开影像
        if not ds:
            sys.exit(0)
        # 创建坐标系
        srs = osr.SpatialReference()
        srs.SetWellKnownGeogCS('WGS84')
        # 相关信息
        rows = ds.RasterYSize  # 行数
        cols = ds.RasterXSize  # 列数
        # 创建地面控制点：经度、纬度、z，照片列数，照片行数
        gcps = [
            gdal.GCP(y1, x2, 0, 0, 0),  # 左上
            gdal.GCP(y2, x2, 0, cols - 1, 0),  # 右上
            gdal.GCP(y1, x1, 0, 0, rows - 1),  # 左下
            gdal.GCP(y2, x1, 0, cols - 1, rows - 1)  # 右下
        ]
        ds.SetGCPs(gcps, srs.ExportToWkt())
        # 确保在数据集上设置了地理变化和投影信息
        ds.SetProjection(srs.ExportToWkt() )
        ds.SetGeoTransform(gdal.GCPsToGeoTransform(gcps) )
        subimgs.append(tif_fp) #加入到subimgs，准备拼接
        del ds

    # 对registration_dir内的数据进行拼接
    out_fn = os.path.join(mosaic_dir, "out.tif")
    params = {
        "-o": out_fn,
        "input_files": subimgs
    }
    from gdal_merge import main_by_params
    main_by_params(params)

    pass
