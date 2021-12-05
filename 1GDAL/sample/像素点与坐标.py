# coding:utf-8
# https://cloud.tencent.com/developer/article/1386146

try:
    from osgeo import gdal
except ImportError:
    import gdal

try:
    from osgeo import osr
except ImportError:
    import osr

import numpy as np

'''input parameters
'''
in_fp = r".\3GeoPandas+RasterIO\土楼分析(点数据与DEM)\tmp\a1_utm50.tif"

def getSRSPair(dataset):
    '''
    获得给定数据的投影参考系和地理参考系
    :param dataset: GDAL地理数据
    :return: 投影参考系和地理参考系
    '''
    prosrs = osr.SpatialReference()
    prosrs.ImportFromWkt(dataset.GetProjection())
    geosrs = prosrs.CloneGeogCS()
    return prosrs, geosrs

def geo2lonlat(dataset, x, y):
    '''
    将投影坐标转为经纬度坐标（具体的投影坐标系由给定数据确定）
    :param dataset: GDAL地理数据
    :param x: 投影坐标x
    :param y: 投影坐标y
    :return: 经纬度(lon, lat)
    '''
    prosrs, geosrs = getSRSPair(dataset)
    ct = osr.CoordinateTransformation(prosrs, geosrs)
    coords = ct.TransformPoint(x, y)    #(纬度, 经度, 高程)。例(24.890063025511623, 116.58402231767289, z)
    return coords[:2][::-1] #逆序，变成（经度，纬度）

def lonlat2geo(dataset, lon, lat):
    '''
    将经纬度坐标转为投影坐标（具体的投影坐标系由给定数据确定）
    :param dataset: GDAL地理数据
    :param lon: 地理坐标lon经度
    :param lat: 地理坐标lat纬度
    :return: 经纬度坐标(lon, lat)对应的投影坐标
    '''
    prosrs, geosrs = getSRSPair(dataset)
    ct = osr.CoordinateTransformation(geosrs, prosrs)
    coords = ct.TransformPoint(lat, lon)
    return coords[:2]

def imagexy2geo(dataset, row, col):
    '''
    根据GDAL的六参数模型将影像图上坐标（行列号）转为投影坐标或地理坐标（根据具体数据的坐标系统转换）
    :param dataset: GDAL地理数据
    :param row: 像素的行号
    :param col: 像素的列号
    :return: 行列号(row, col)对应的投影坐标或地理坐标(x, y)
    '''
    trans = dataset.GetGeoTransform()
    px = trans[0] + col * trans[1] + row * trans[2]
    py = trans[3] + col * trans[4] + row * trans[5]
    return px, py

def geo2imagexy(dataset, x, y):
    '''
    根据GDAL的六 参数模型将给定的投影或地理坐标转为影像图上坐标（行列号）
    :param dataset: GDAL地理数据
    :param x: 投影或地理坐标x
    :param y: 投影或地理坐标y
    :return: 影坐标或地理坐标(x, y)对应的影像图上行列号(row, col)
    '''
    trans = dataset.GetGeoTransform()
    a = np.array([[trans[1], trans[2]], [trans[4], trans[5]]])
    b = np.array([x - trans[0], y - trans[3]])
    return np.linalg.solve(a, b)  # 使用numpy的linalg.solve进行二元一次方程的求解

def geo2imagexy_v2(dataset, x, y):
    """
    版本二：地理坐标 => 像素坐标
    """
    geoTrans = dataset.GetGeoTransform()
    ulx = geoTrans[0]
    uly = geoTrans[3]
    xDist = geoTrans[1]
    yDist = geoTrans[5]
    rtnX = geoTrans[2]
    rtnY = geoTrans[4]
    pixel = int((x - ulx) / xDist)
    line = int((uly - y) / abs(yDist))
    return (pixel, line)

if __name__ == '__main__':
    gdal.AllRegister()
    dataset = gdal.Open(in_fp)
    print(f"[数据投影]\t {dataset.GetProjection()}")
    print("")

    print(f"[数据大小]\t 行：{dataset.RasterYSize}\t列：{dataset.RasterXSize}")
    print("")

    x = 457986.299
    y = 2752838.863
    lon = 116.58402231767289    #经度，longitude
    lat = 24.890063025511623    #纬度：latitude
    row = 2399
    col = 3751
    
    print('[投影坐标] (x,y) => [经纬度] (lon, lat)')
    print(f"({x}, {y}) => {geo2lonlat(dataset, x, y)}\n")

    print('[经纬度] (lon, lat) => [投影坐标] (x, y)')
    print(f"({lon}, {lat}) => {lonlat2geo(dataset, lon, lat)}\n")

    print('[图上坐标] (行，列) -> [投影坐标] (x, y)')
    print(f"({row}, {col}) => {imagexy2geo(dataset, row, col)}\n")

    print('[投影坐标] (x,y) -> [图上坐标] (行，列)')
    print(f"({x}, {y}) => {geo2imagexy(dataset, x, y)}\n")

    print('[投影坐标] (x,y) -> [图上坐标] (行，列) ——v2')
    print(f"({x}, {y}) => {geo2imagexy_v2(dataset, x, y)}\n")