# coding:utf-8
# https://stackoverflow.com/questions/30740046/calculate-distance-to-nearest-feature-with-geopandas
import geopandas

# read geodata for five nyc boroughs
gdf_nyc = geopandas.read_file(geopandas.datasets.get_path('nybb'))
# read geodata for international cities
gdf_cities = geopandas.read_file(geopandas.datasets.get_path('naturalearth_cities'))

# 计算距离之前，需要把单位转成米（即投影坐标系）
gdf_nyc.to_crs(epsg=3857, inplace=True)
gdf_cities.to_crs(epsg=3857, inplace=True)

# 获得每个纽约市行政区（多边形）与其最近的国际城市（点）之间的最小距离
gdf_nyc["min_dist_to_cities"] = gdf_nyc.geometry.apply(lambda x: gdf_cities.distance(x).min())

# 每个国际城市与其最近的纽约市行政区之间的最小距离
gdf_cities["min_dist_to_nyc"] = gdf_cities.geometry.apply(lambda x: gdf_nyc.distance(x).min())

# 求最小距离的那个点


input("Enter any key to end.")