# -*- coding: utf-8 -*-
# @Time    : 2019/12/26 21:48
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : intersect
# @Software: PyCharm
# @Version :
# @Desc    :

from osgeo import ogr

path1 = r"D:\mycode\PythonGIS\workspace\data\2019.json"
path2 = r"D:\mycode\PythonGIS\workspace\data\SelectPolygon.json"
out_path = r"D:\mycode\PythonGIS\workspace\data\intersection.json"

ds1 = ogr.Open(path1)
ly1 = ds1.GetLayer(0)

ds2 = ogr.Open(path2)
ly2 = ds2.GetLayer(0)

driver = ogr.GetDriverByName('GeoJSON')
newds = driver.CreateDataSource(out_path) #首先得有数据源
result_ly  = newds.CopyLayer(ly2, 'result') #复制图层，返回指针

ly1.Intersection(ly2, result_ly)
newds.Destroy() #对newds进行Destroy()操作，才能将数据写入磁盘