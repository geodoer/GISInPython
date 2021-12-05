# https://rasterio.readthedocs.io/en/latest/topics/reproject.html
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

in_fp = r".\3GeoPandas+RasterIO\土楼分析(点数据与DEM)\data\a1"
dst_crs = 'EPSG:32650'
out_fp = r".\3GeoPandas+RasterIO\土楼分析(点数据与DEM)\tmp\a1_utm50.tif"

with rasterio.open(in_fp) as src:
    # 计算在新空间参考系下的仿射变换参数，图像尺寸
    transform, width, height = calculate_default_transform(
        src.crs,        # 输入坐标系
        dst_crs,        # 输出坐标系
        src.width,      # 输入图像宽
        src.height,     # 输入图像高
        *src.bounds)    # 输入数据源的图像范围
    
    # 更新数据集的元数据信息
    kwargs = src.meta.copy()
    kwargs.update({
        'crs': dst_crs,
        'transform': transform,
        'width': width,
        'height': height
    })
    kwargs.pop("driver") #防止in_fp与out_fp的格式不同

    # 重投影并写入数据
    with rasterio.open(out_fp, 'w', **kwargs) as dst: #这里可传入driver，但也可根据out_fp自动获取
        for i in range(1, src.count + 1):   # 遍历每个图层，通常只需要第一层即可（下标从1开始）
            #重投影
            reproject(
                # 源文件参数
                source=rasterio.band(src, i),
                src_transform=src.transform,
                src_crs=src.crs,
                # 目标文件参数
                destination=rasterio.band(dst, i),  #如果你不想保存到文件，直接传一个ndarray也行
                dst_transform=transform,
                dst_crs=dst_crs,
                # 其它配置
                # resampling=Resampling.nearest,  #重采样策略
                # num_threads=2   #线程数
            )