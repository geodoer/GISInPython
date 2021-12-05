# 无坐标系图片配准、拼接
## 背景
【背景】采集到3幅雷达降水图
- .png格式
- 无坐标系
- 信息有：四个角坐标，但坐标是GCJ02标准

【需求】将3个雷达降水图拼接成一个图

【步骤】
1. 将四个角坐标（GCJ02）转成WGS84标准
2. png转成tif格式
3. 通过4个角点坐标（WGS84标准）对tif数据进行配准
4. 对3幅图进行拼接：按时间顺序拼接
    - 重叠区域处理：后面的图幅盖掉前面的图幅

## 文件夹说明
【data】

1. original
    - 原始数据
    - 图像信息查看：infos.json
2. registration：配准数据
3. mosaic：融合数据

【坐标系】经纬度与numpy坐标系比对图

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190410170320638.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)

# 代码
```python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/10 11:09
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : __init__
# @Software: PyCharm
# @Version :
# @Desc    :

import sys


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
    from coordinate_conversion import gcj02towgs84_extent
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
    import gdal
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
    # 【方法一】
    params = {
        "-o": out_fn,
        "input_files": subimgs
    }
    from gdal_merge import main_by_params
    main_by_params(params)

    #【方法二】
    # from mosaic import mosaic_files
    # mosaic_files(subimgs, out_fn)

    pass

```