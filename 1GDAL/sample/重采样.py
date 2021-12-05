# https://blog.csdn.net/gisuuser/article/details/106304155
from osgeo import gdal, gdalconst
import os
import numpy as np
 
 
def resampling(source_file, target_file, scale=1.0):
    """
    影像重采样
    :param source_file: 源文件
    :param target_file: 输出影像
    :param scale: 像元缩放比例
    :return:
    """
    dataset = gdal.Open(source_file, gdalconst.GA_ReadOnly)
    band_count = dataset.RasterCount  # 波段数
 
    if band_count == 0 or not scale > 0:
        print("参数异常")
        return
 
    cols = dataset.RasterXSize  # 列数
    rows = dataset.RasterYSize  # 行数
    cols = int(cols * scale)  # 计算新的行列数
    rows = int(rows * scale)
 
    geotrans = list(dataset.GetGeoTransform())
    print(dataset.GetGeoTransform())
    print(geotrans)
    geotrans[1] = geotrans[1] / scale  # 像元宽度变为原来的scale倍
    geotrans[5] = geotrans[5] / scale  # 像元高度变为原来的scale倍
    print(geotrans)
 
    if os.path.exists(target_file) and os.path.isfile(target_file):  # 如果已存在同名影像
        os.remove(target_file)  # 则删除之
 
    band1 = dataset.GetRasterBand(1)
    data_type = band1.DataType
    target = dataset.GetDriver().Create(target_file, xsize=cols, ysize=rows, bands=band_count,
                                        eType=data_type)
    target.SetProjection(dataset.GetProjection())  # 设置投影坐标
    target.SetGeoTransform(geotrans)  # 设置地理变换参数
    total = band_count + 1
    for index in range(1, total):
        # 读取波段数据
        print("正在写入" + str(index) + "波段")
        data = dataset.GetRasterBand(index).ReadAsArray(buf_xsize=cols, buf_ysize=rows)
        out_band = target.GetRasterBand(index)
        out_band.SetNoDataValue(dataset.GetRasterBand(index).GetNoDataValue())
        out_band.WriteArray(data)  # 写入数据到新影像中
        out_band.FlushCache()
        out_band.ComputeBandStats(False)  # 计算统计信息
    print("正在写入完成")
    del dataset
    del target
 
 
if __name__ == "__main__":
    source_file = r"E:\商丘yx\相交4.tiff"
    target_file = r"E:\商丘yx\相交411.tiff"
    resampling(source_file, target_file, scale=1.1)
    target_file = r"E:\商丘yx\相交05.tiff"
    resampling(source_file, target_file, scale=0.5)
 