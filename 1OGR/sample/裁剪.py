# -*- coding: utf-8 -*-
# @Time    : 2019/4/14 18:00
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : cut
# @Software: PyCharm
# @Version :
# @Desc    :

from osgeo import ogr
import os

# =======================================================
#           文件级别裁剪
def clipping_file(input_file, cut_file, out_file):
    # get cutting geometry
    try:
        cut_ds = ogr.Open(cut_file)
        cut_lyr = cut_ds.GetLayer(0)
        cut_feat = cut_lyr.GetNextFeature()
        cut_geom = cut_feat.geometry()
        if cut_geom.GetGeometryType() != ogr.wkbPolygon:
            return "[Input ERROR] the geometry type of cut_file isn't Polygon..."
    except:
        return "[Input ERROR] cut_file error..."

    try:
        input_ds = ogr.Open(input_file)
        input_lyr = input_ds.GetLayer(0)
        input_lyr.SetSpatialFilter(cut_geom)
    except:
        return "[Input ERROR] input_file error..."

    try:
        driver = ogr.GetDriverByName("ESRI Shapefile")
        newds = driver.CreateDataSource(out_file)
        pt_layer = newds.CopyLayer(input_lyr, 'copylayer')  # 复制图层，返回指针
        newds.Destroy()  # 对newds进行Destroy()操作，才能将数据写入磁盘
    except:
        return "[Cut ERROR] Cut out failure..."

    return out_file

# ========================================================
#       图层级别裁剪
def clipping_layer(input_file, cut_geomtry):
    """
    :param input_file: 输入的shp文件
    :param cut_geomtry: 裁剪的geometry
    :return: 返回layer
    """
    pass

if __name__ == '__main__':
    input_file = r'E:\SAR\ps\geocoding\4PS_20190405_PS_75_166.shp'
    cut_file = r"E:\SAR\ps\xiamen.shp"
    out_file = r"E:\SAR\tmp\cut_result.shp"

    clipping_file(input_file, cut_file, out_file)