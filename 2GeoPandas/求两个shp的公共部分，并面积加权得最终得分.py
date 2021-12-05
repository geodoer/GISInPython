# -*- coding: utf-8 -*-
# @Time    : 2019/12/28 20:27
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : overlap
# @Software: PyCharm
# @Version :
# @Desc    : 两shp相交，并计算结果的面积，再用面积加权计算最后价格
import geopandas
import os

env = r'D:\mycode\PythonGIS\workspace\data'
path1 = os.path.join(env, "2019.shp")           #2019的地价
path2 = os.path.join(env, "SelectPoylgon.shp")  #感兴趣区域
out_path = os.path.join(env, "inter.shp")      #结果

gdf1 = geopandas.read_file(path1)
gdf2 = geopandas.read_file(path2)

# 相交
land_price_gdf = geopandas.overlay(gdf1, gdf2, how="intersection")
# 计算面积
land_price_gdf = land_price_gdf.to_crs({'init': 'epsg:32650'}) #转成投影坐标后，才能算出正确的面积（示例，转为墨卡托投影）
land_price_gdf['area'] = land_price_gdf.apply(lambda row: row.geometry.area, axis=1)
# 计算最终地价
sum = land_price_gdf['area'].sum()                              #总面积
land_price_gdf['area_weight'] = land_price_gdf['area']/sum      #面积权重
land_price_gdf['total_price'] = land_price_gdf['land_price']    #原来的总价格
land_price_gdf['land_price'] = land_price_gdf['area_weight']*land_price_gdf['total_price'] #相交后的价格
price = land_price_gdf['land_price'].sum()  #总地价
print("总价格", price)
# 保存
land_price_gdf.to_file(out_path, encoding="utf-8")

