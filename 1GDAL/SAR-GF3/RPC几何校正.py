# -*- coding: utf-8 -*-
# 参考文章：https://blog.csdn.net/lidahuilidahui/article/details/116659207

from osgeo import gdal
import os
import numpy

'''
Input Paramters
'''
in_fp = r"F:\05Nanjing\02算法\2021_12_03高分三号\2091067_Rennes\GF3_MDJ_QPSI_002118_W1.5_N48.3_20170103_L1A_HH_L10002091067.tiff"
out_dir = r"F:\05Nanjing\02算法\2021_12_03高分三号\result"
# DEM tif文件的路径
# 注意DEM的覆盖范围要比原影像的范围大，此外，DEM不能有缺失值，有缺失值会报错
# 通常DEM在水域是没有值的（即缺失值的情况），因此需要将其填充设置为0，否则在RPC校正时会报错
# 这里使用的DEM是填充0值后的SRTM V4.1 3秒弧度的DEM(分辨率为90m)
# 请网上自行搜索下载GF-3 SAR影像对应的DEM文件（GeoTiff格式， WGS84坐标系）
dem_tif_file = r'F:\05Nanjing\02算法\2021_12_03高分三号\RPC_GF3_DEM\srtm_36_03\srtm_36_03.tif'

basename = os.path.basename(in_fp)
basename,ext = os.path.splitext(basename)

def get_rpc_fp(data_fp):
    ext = os.path.splitext(data_fp)[1]
    return data_fp.replace(ext, ".rpc")

# 解析.rpc文件的函数
def parse_rpc_file(rpc_file):
    # rpc_file:.rpc文件的绝对路径
    # rpc_dict：符号RPC域下的16个关键字的字典
    # 参考网址：http://geotiff.maptools.org/rpc_prop.html；
    # https://www.osgeo.cn/gdal/development/rfc/rfc22_rpc.html

    rpc_dict = {}
    with open(rpc_file) as f:
        text = f.read()

    # .rpc文件中的RPC关键词
    words = ['errBias', 'errRand', 'lineOffset', 'sampOffset', 'latOffset',
             'longOffset', 'heightOffset', 'lineScale', 'sampScale', 'latScale',
             'longScale', 'heightScale', 'lineNumCoef', 'lineDenCoef','sampNumCoef', 'sampDenCoef',]

    # GDAL库对应的RPC关键词
    keys = ['ERR_BIAS', 'ERR_RAND', 'LINE_OFF', 'SAMP_OFF', 'LAT_OFF', 'LONG_OFF',
            'HEIGHT_OFF', 'LINE_SCALE', 'SAMP_SCALE', 'LAT_SCALE',
            'LONG_SCALE', 'HEIGHT_SCALE', 'LINE_NUM_COEFF', 'LINE_DEN_COEFF',
            'SAMP_NUM_COEFF', 'SAMP_DEN_COEFF']

    for old, new in zip(words, keys):
        text = text.replace(old, new)
    # 以‘;\n’作为分隔符
    text_list = text.split(';\n')
    # 删掉无用的行
    text_list = text_list[3:-2]
    #
    text_list[0] = text_list[0].split('\n')[1]
    # 去掉制表符、换行符、空格
    text_list = [item.strip('\t').replace('\n', '').replace(' ', '') for item in text_list]

    for item in text_list:
        # 去掉‘=’
        key, value = item.split('=')
        # 去掉多余的括号‘(’，‘)’
        if '(' in value:
            value = value.replace('(', '').replace(')', '')
        rpc_dict[key] = value

    for key in keys[:12]:
        # 为正数添加符号‘+’
        if not rpc_dict[key].startswith('-'):
            rpc_dict[key] = '+' + rpc_dict[key]
        # 为归一化项和误差标志添加单位
        if key in ['LAT_OFF', 'LONG_OFF', 'LAT_SCALE', 'LONG_SCALE']:
            rpc_dict[key] = rpc_dict[key] + ' degrees'
        if key in ['LINE_OFF', 'SAMP_OFF', 'LINE_SCALE', 'SAMP_SCALE']:
            rpc_dict[key] = rpc_dict[key] + ' pixels'
        if key in ['ERR_BIAS', 'ERR_RAND', 'HEIGHT_OFF', 'HEIGHT_SCALE']:
            rpc_dict[key] = rpc_dict[key] + ' meters'

    # 处理有理函数项
    for key in keys[-4:]:
        values = []
        for item in rpc_dict[key].split(','):
            #print(item)
            if not item.startswith('-'):
                values.append('+'+item)
            else:
                values.append(item)
            rpc_dict[key] = ' '.join(values)
    return rpc_dict

# 全局设置
gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES") #支持文件名称及路径内的中文
gdal.SetConfigOption("SHAPE_ENCODING", "GBK")        #支持属性字段中的中文

old_ds = gdal.Open(in_fp)

# 创建临时的tif文件，并写入RPC域的文件
rpc_out_fp = os.path.join(out_dir, f"{basename}_rpc{ext}")
out_ds = old_ds.GetDriver().CreateCopy(rpc_out_fp, old_ds)
#out_ds.SetProjection('')
# 向tif影像写入rpc域信息
# 注意，这里虽然写入了RPC域信息，但实际影像还没有进行实际的RPC校正
# 尽管有些RS/GIS能加载RPC域信息，并进行动态校正
rpc_file = get_rpc_fp(in_fp)
rpc_dict = parse_rpc_file(rpc_file)
for k in rpc_dict.keys():
    out_ds.SetMetadataItem(k, rpc_dict[k], 'RPC')

out_ds.FlushCache()
del old_ds, out_ds
print(f'将RPC写入到文件中：{rpc_out_fp}')

## 设置rpc校正的参数
# 原图像和输出影像缺失值设置为0，输出影像坐标系为WGS84(EPSG:4326), 重采样方法为双线性插值（bilinear，还有最邻近‘near’、三次卷积‘cubic’等可选)
# RPC_DEM=G:\\test_GF3\\2599253_San_Francisco\\Geometric_Correction\\srtm_12_05_fill_nodata.tif 中
# G:\\test_GF3\\2599253_San_Francisco\\Geometric_Correction\\srtm_12_05_fill_nodata.tif为覆盖原影像范围的DEM
# 注意DEM的覆盖范围要比原影像的范围大，此外，DEM不能有缺失值，有缺失值会报错
# 通常DEM在水域是没有值的（即缺失值的情况），因此需要将其填充设置为0，否则在RPC校正时会报错
# 这里使用的DEM是填充0值后的SRTM V4.1 3秒弧度的DEM(分辨率为90m)
# RPC_DEMINTERPOLATION=bilinear  表示对DEM重采样使用双线性插值算法
wo = gdal.WarpOptions(srcNodata=0, dstNodata=0, dstSRS='EPSG:4326', resampleAlg='bilinear', rpc=True, warpOptions=["INIT_DEST=NO_DATA"],
                 transformerOptions=["RPC_DEM=%s"%(dem_tif_file), "RPC_DEMINTERPOLATION=bilinear"])

## 对于全海域的影像或者不使用DEM校正的话，可以将transformerOptions有关的RPC DEM关键字删掉
## 即将上面gdal.WarpOptions注释掉，将下面的语句取消注释，无DEM时，影像范围的高程默认全为0
# wo = gdal.WarpOptions(srcNodata=0, dstNodata=0, dstSRS='epsg:4326',resampleAlg='bilinear', rpc=True, warpOptions=["INIT_DEST=NO_DATA"])

result_fp = os.path.join(out_dir, f"{basename}_GeometricCorrection{ext}")
# 执行rpc校正
wr = gdal.Warp(result_fp,  rpc_out_fp, options=wo)
print(f'得到RPC校正后的影像：{result_fp}')