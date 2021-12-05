# -*- encoding: utf-8 -*-
"""
@File    : Landsat8_temperature_retrieval.py
@Time    : 2020/4/19 17:53
@Author  : GeoDoer
@Email   : geodoer@163.com
@Software: PyCharm
@Func   :   Landsat8 温度反演，单窗算法
@Desc   :   python2 arcpy
"""

import os
import re
import arcpy, string
from arcpy.sa import *
import math

arcpy.CheckOutExtension("spatial")
# arcpy.env.nodata = 0    #无用

''' 根据landsat 8文件夹，获得文件列表
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
        elif fn.endswith("B8.tif") or fn.endswith("B8.TIF"):
            landsat_files['B8'] = fp
        elif fn.endswith("B9.tif") or fn.endswith("B9.TIF"):
            landsat_files['B9'] = fp
        elif fn.endswith("B10.tif") or fn.endswith("B10.TIF"):
            landsat_files['B10'] = fp
        elif fn.endswith("B11.tif") or fn.endswith("B11.TIF"):
            landsat_files['B11'] = fp

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
    file = os.path.basename(fp)
    ext = file.split('.')[-1]
    fn = file.replace("." + ext, "")
    out_fp = os.path.join(out_dir, '{}_clip.{}'.format( fn, ext))
    print("[clip] {} -> {}".format(fp, out_fp))

    if os.path.exists(out_fp):
        return out_fp

    # outExtractByMask = arcpy.sa.ExtractByMask(fp, shp_fp) #不建议使用掩膜
    # outExtractByMask.save(out_fp)
    arcpy.Clip_management(in_raster=fp,  out_raster=out_fp, in_template_dataset=shp_fp, nodata_value=0, clipping_geometry=True, maintain_clipping_extent=False)   #不重采样
    return out_fp


''' 获取影像头文件中的数据
fp          头文件路径
regex_str   正则规则，举例："DATE_ACQUIRED = (.*)"
'''
def get_str_from_meta(tm5_dir, regex_str):
    fp = None
    for fn in os.listdir(tm5_dir):
        if fn.endswith("_MTL.txt"):
            fp = os.path.join(tm5_dir, fn)
            break

    if fp is None: return None

    with open(fp, 'r') as f:
        filestr = f.read()
        result = re.findall(regex_str, filestr)
        if len(result)==1:
            return result[0]

    return None

def landsat_ndvi(landsat_files, out_dir):
    out_fp = os.path.join(out_dir, "ndvi.tif")

    if os.path.exists(out_fp):
        return out_fp

    NIR = arcpy.Raster( landsat_files["B5"] )
    R = arcpy.Raster( landsat_files["B4"] )
    num = arcpy.sa.Float(NIR - R)
    denom = arcpy.sa.Float(NIR + R)
    ndvi = arcpy.sa.Divide(num, denom)
    ndvi.save(out_fp)
    return out_fp

def cal_pv(ndvi_fp, out_dir):
    out_fp = os.path.join(out_dir, "pv.tif")

    if os.path.exists(out_fp):
        return out_fp

    ndvi = arcpy.Raster(ndvi_fp)
    formula =(((ndvi - 0.05) * (ndvi - 0.05)) / (0.65*0.65) )
    pv = Con(ndvi < 0.05, 0,
             Con(ndvi <= 0.7, formula, 1))
    pv.save(out_fp)
    return out_fp

def cal_x(pv_fp, class_tif, out_dir):
    out_fp = os.path.join(out_dir, "x.tif")
    ndvi = arcpy.Raster(ndvi_fp)
    pv = arcpy.Raster(pv_fp)
    if os.path.exists(out_fp):
        return out_fp

    # 算法一
    #buidling =0.9589 + 0.086 * pv - 0.0671 * pv * pv
    #surface = 0.9625 + 0.0614 * pv - 0.0461 * pv * pv
    #x = Con(ndvi <= 0, 0.995,
     #        Con(ndvi < 0.7, buidling, surface))

    # 算法二
    cls = arcpy.Raster(class_tif)   #监督分类图像
    water = Con(cls==3, 0.995, 0)
    buidling = Con(cls==1, 0.9589+0.086*pv-0.0671*pv*pv, 0)
    surface = Con(cls==2, 0.9625+0.0614*pv-0.0461*pv*pv, 0)
    x = water + buidling + surface

    x = arcpy.sa.SetNull(x==0, x)
    x.save(out_fp)
    return out_fp

def cal_T6(tm5_dir, landsat_files, out_dir):
    out_fp = os.path.join(out_dir, "T10.tif")

    if os.path.exists(out_fp):
        return out_fp

    DN = arcpy.Raster(landsat_files["B10"])
    M = float(get_str_from_meta(tm5_dir, "RADIANCE_MULT_BAND_10 = (.*)"))
    A = float(get_str_from_meta(tm5_dir, "RADIANCE_ADD_BAND_10 = (.*)"))
    L = A + M * DN

    k1 = float( get_str_from_meta(tm5_dir, "K1_CONSTANT_BAND_10 = (.*)") )
    k2 = float( get_str_from_meta(tm5_dir, "K2_CONSTANT_BAND_10 = (.*)") )
    T6 = k2 /( Ln(1+k1/L))
    T6.save(out_fp)
    return out_fp

def cal_Ta(T0, region):
    if region == 1:
        return 16.011 + 0.92621*T0
    elif region == 2:
        return 19.270 + 0.91118*T0
    elif region == 3:
        return 17.976 + 0.91715*T0
    elif region == 4:
        return 25.939 + 0.88045*T0



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
        "TM5Dir": r"F:\lu\20191211\LC08_L1TP_119043_20191211_20191217_01_T1",
        "clip_fp" : r"F:\lu\xiamen\xm-shapefile\xmbj.shp",
        "class_tif" : r"F:\lu\20191211\class\20191211class_v_mj.dat",  #监督分类结果：1为建筑物、2为自然表面、3为水体
        "f" : 0.85,          #大气透射率
        "T0" : 288.15,           #温度
        "region" : 2,        #研究区：1中纬度夏季大气，2中纬度冬季大气，3热带地区，4美国1976标准大气公式
        "project_dir": r"F:\lu\20191211"
    }

    # 获得参数
    tm5_dir = config["TM5Dir"]
    project_dir = config["project_dir"]
    clip_fp = config["clip_fp"]
    class_tif = config["class_tif"]
    f = config["f"]  # 大气透射率
    T0 = config["T0"]
    region = config["region"]

    # 输出文件夹
    clip_dir = os.path.join(project_dir, "clip")
    mkdir(clip_dir)

    # 获得文件
    landsat_files = get_tm5_filelist(tm5_dir)
    print(landsat_files)

    # 裁剪
    if clip_fp != "":
        landsat_files = clip_files(landsat_files, clip_fp, clip_dir)
        print(landsat_files)

    ndvi_fp = landsat_ndvi(landsat_files, project_dir)
    pv_fp = cal_pv(ndvi_fp, project_dir)          #植被覆盖度
    x_fp = cal_x(pv_fp, class_tif, project_dir)   #地表比辐射率
    T6_fp = cal_T6(tm5_dir, landsat_files, project_dir)
    Ta = cal_Ta(T0, region)

    x = arcpy.Raster(x_fp)
    T6 = arcpy.Raster(T6_fp)
    C = f*x
    D = (1-f)*( 1+(1-x)*f )

    a = -67.355351
    b = 0.458606

    Ts = Con(C==0 , 0, ( a*(1-C-D) + (b*(1-C-D)+C+D)*T6 - D*Ta ) / C - 273.15)
    out_fp = os.path.join(project_dir, "Ts.tif")
    Ts.save(out_fp)