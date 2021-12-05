# coding:utf-8
import geopandas

path = r"D:\mycode\PythonGIS\workspace\data\2019.shp"
gdf = geopandas.read_file(path)
gdf = gdf.to_crs({'init': 'epsg:4326'})
gdf.to_file(path)