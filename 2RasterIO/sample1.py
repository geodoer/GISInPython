# 原文链接：https://zhuanlan.zhihu.com/p/278206958
import rasterio
import os
import numpy as np

data_dir = "data"
fp = os.path.join(data_dir, "Helsinki_masked_p188r018_7t20020529_z34__LV-FIN.tif")

raster = rasterio.open(fp)
type(raster)

###################
# 查看信息
###################
raster.crs # 坐标系
raster.transform # 仿射变换
(raster.width,raster.height) # 维度
raster.bounds #包围盒
raster.count # 波段
raster.nodatavals # 缺失值
raster.dirver # 数据格式

# 上面的所有信息，也可以通过raster.meta一次展示
raster.meta

###################
# 查看波段的具体的数值以及统计信息
###################
band1 = raster.read(1) # 第一波段属性值

# 所有波段
array = raster.read()
# 统计每个波段的信息
stats = []
for band in array:
    stats.append({
        'min': band.min(),
        'mean': band.mean(),
        'median': np.median(band),
        'max': band.max()})
# 展示统计信息
stats

###################
# 可视化
###################
import matplotlib.pyplot as plt
from rasterio.plot import show

# band 1
show((raster, 1))

fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, nrows=1, figsize=(10, 4), sharey=True)

# rgb 展示
show((raster, 4), cmap='Reds', ax=ax1)
show((raster, 3), cmap='Greens', ax=ax2)
show((raster, 1), cmap='Blues', ax=ax3)

# 添加标题
ax1.set_title("Red")
ax2.set_title("Green")
ax3.set_title("Blue")

###################
# 图像合成
###################
# 假彩色合成
nir,red,green = raster.read(4),raster.read(3),raster.read(2)
def normalize(array):
    """Normalizes numpy arrays into scale 0.0 - 1.0"""
    array_min, array_max = array.min(), array.max()
    return ((array - array_min)/(array_max - array_min))
# 标准化
nirn,redn,greenn = normalize(nir),normalize(red),normalize(green)
# 图像合成
nrg = np.dstack((nirn, redn, greenn))
plt.imshow(nrg)

###################
# 栅格属性的直方图
###################
# 栅格
from rasterio.plot import show_hist
show_hist(raster, bins=50, lw=0.0, stacked=False, alpha=0.3,
      histtype='stepfilled', title="Histogram")

###################
# 用矢量裁剪栅格
###################
from rasterio.mask import mask
from shapely.geometry import box
import geopandas as gpd
from fiona.crs import from_epsg
import pycrs

# 保存
out_tif = os.path.join(data_dir, "Helsinki_Masked.tif")

# 根据raster边界创建边界
minx, miny = 700000,6660000
maxx, maxy = 730000, 6690000
bbox = box(minx, miny, maxx, maxy)
geo = gpd.GeoDataFrame({'geometry': bbox}, index=[0], crs=raster.crs.data)
# geo.plot() 
def getFeatures(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]

coords = getFeatures(geo)

# 裁剪
out_img, out_transform = mask(dataset=raster, shapes=coords, crop=True)

# 输出属性信息
out_meta = raster.meta.copy()
out_meta.update({"driver": "GTiff",
                 "height": out_img.shape[1],
                 "width": out_img.shape[2],
                 "transform": out_transform,
                 "crs":raster.crs}
                         )
with rasterio.open(out_tif, "w", **out_meta) as dest:
        dest.write(out_img)

###################
# 计算NDVI
###################
# red波段
red = raster.read(3)
# 近红外-NIR波段
nir = raster.read(4)
# 数值类型转换
red = red.astype('f4')
nir = nir.astype('f4')

np.seterr(divide='ignore', invalid='ignore')
# ndvi 计算
ndvi = (nir - red) / (nir + red)
# 
plt.imshow(ndvi, cmap='terrain_r')
# 添加colorbar
plt.colorbar()