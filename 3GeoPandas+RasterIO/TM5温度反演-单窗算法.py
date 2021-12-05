# -*- encoding: utf-8 -*-
"""
@File    : tm5_temperature_retrieval.py
@Time    : 2020/4/19 17:53
@Author  : GeoDoer
@Email   : geodoer@163.com
@Software: PyCharm
@Func   :
@Desc   :   Landsat5 TM温度反演，单窗算法
"""

import os
import re
import numpy as np
import rasterio
from rasterio import mask
import geopandas

''' 根据landsat TM5文件夹，获得TM5文件列表
'''
def get_tm5_filelist(landsat_dir):
    landsat_files = {}
    fns = os.listdir(landsat_dir)
    for fn in fns:
        fp = os.path.join(landsat_dir, fn)
        if fn.endswith("B1.tif") or fn.endswith("B1.TIF"):
            landsat_files["B1"] = fp
        elif fn.endswith("B2.tif") or fn.endswith("B2.TIF"):
            landsat_files['B2'] = fp
        elif fn.endswith("B3.tif") or fn.endswith("B3.TIF"):
            landsat_files['B3'] = fp
        elif fn.endswith("B4.tif") or fn.endswith("B4.TIF"):
            landsat_files['B4'] = fp
        elif fn.endswith("B5.tif") or fn.endswith("B5.TIF"):
            landsat_files['B5'] = fp
        elif fn.endswith("B6.tif") or fn.endswith("B6.TIF"):
            landsat_files['B6'] = fp
        elif fn.endswith("B7.tif") or fn.endswith("B7.TIF"):
            landsat_files['B7'] = fp

    return landsat_files

'''裁剪文件列表
'''
def clip_files(filelist, shp_fp, out_dir):
    cliplist = {}

    for key in filelist:
        value = filelist[key]
        out_fp = clip(value, shp_fp, out_dir)
        cliplist[key] = out_fp

    return cliplist

'''裁剪
'''
def clip(fp, shp_fp, out_dir):
    (fn, ext) = os.path.splitext(fp)
    out_fp = os.path.join(out_dir, '{}_clip.'.format(ext))

    rasterdata = rasterio.open(fp)  # 读栅格

    shpdata = geopandas.read_file(shp_fp)  # 读shp
    shpdata = shpdata.to_crs(rasterdata.crs)  # 统一投影
    features = [shpdata.geometry.__geo_interface__]
    print(features)

    # 影像裁剪
    out_image, out_transform = rasterio.mask.mask(rasterdata, features, all_touched=True, crop=True, nodata=rasterdata.nodata)
    out_meta = rasterdata.meta.copy()
    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})
    band_mask = rasterio.open(out_fp, "w", **out_meta)
    band_mask.write(out_image)
    return out_fp


''' 获取影像头文件中的数据
fp          头文件路径
regex_str   正则规则，举例："DATE_ACQUIRED = (.*)"
'''
def get_str_from_meta(tm5_dir, regex_str):
    fp = None
    for fn in os.listdir(tm5_dir):
        if fn.endswith("_MTL.txt"):
            landsat_files["MTL"] = os.path.join(tm5_dir, fn)
            continue

    if fp is None: return None

    with open(fp, 'r') as f:
        str = f.read()
        match = re.match(regex_str, str, re.M|re.I)
        if match:
            return match.group(1)

    return None

def landsat_ndvi(landsat_files, out_dir):
    out_fp = os.path.join(out_dir, "ndvi.tif")
    # 获取b3
    src = rasterio.open( landsat_files["B3"] )
    b3 = src.read()
    # 获取b4
    b4 = rasterio.open( landsat_files["B4"] ).read()
    # 计算NDVI指数（对除0做特殊处理）
    with np.errstate(divide='ignore', invalid='ignore'):
        ndvi = (b4 - b3) / (b3 + b4)
        ndvi[ndvi == np.inf] = 0
        ndvi = np.nan_to_num(ndvi)
        # 保存数据
        profile = src.profile # 源数据的元信息集合（使用字典结构存储了数据格式，数据类型，数据尺寸，投影定义，仿射变换参数等信息）
        profile.update(
            dtype=ndvi.dtype,
            count=1
        )
        with rasterio.open(out_fp, mode='w', **profile) as dst:
            dst.write(ndvi)
            dst.close()

# Tools
def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)
        print( "[OK] Create Dir:{}".format(path) )
        return True

if __name__ == '__main__':
    config = {
        "TM5Dir": r"F:\lu\20091129\LT05_L1TP_119043_20091129_20161017_01_T1_ANG",
        "clip_fp" : r"F:\lu\xiamen\xm-shapefile\xmbj.shp",
        "project_dir": r"F:\lu\20091129"
    }

    # 获得参数
    tm5_dir = config["TM5Dir"]
    project_dir = config["project_dir"]
    clip_fp = config["clip_fp"]

    # 输出文件夹
    clip_dir = os.path.join(project_dir, "clip")
    mkdir(clip_dir)

    landsat_files = get_tm5_filelist(tm5_dir)
    print(landsat_files)

    clip_files(landsat_files, clip_fp, clip_dir)
    # 裁剪报错

    # landsat_ndvi(landsat_files, out_dir)



    pass