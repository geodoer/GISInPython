# coding:utf-8
import geopandas

path = r"D:\mycode\PythonGIS\workspace\data\2019.shp"

gdf = geopandas.read_file(path)
# 转坐标系
old_crs = gdf.crs
gdf = gdf.to_crs({'init': 'epsg:32650'}) # 转成投影坐标后，才能算出正确的面积（WGS84 UTM North Zone50）
gdf['area'] = gdf.apply(lambda row: row.geometry.area, axis=1) #计算面积
gdf = gdf.to_crs(old_crs)  #转换为原来的坐标系
# 保存
gdf.to_file(path)