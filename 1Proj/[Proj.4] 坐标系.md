[toc]

【PROJ.4】开源GIS最著名的地图投影库，它专注于地图投影的表达，以及转换
【GDAL】GDAL中的投影转换函数（类CoordinateTransformation中的函数）也是动态调用该库函数的

【Python安装】`pip install pyproj`
【网站】
1. proj帮助文档：https://proj4.org/
2. pyproj模块的在线文档：https://code.google.com/p/pyproj


# 初始化Proj对象
```python
# 【方法一】proj字符串
p = pyproj.Proj("+proj=utm +zone=31 +ellps=WGS84")
# 【方法二】proj函数参数
p = pyproj.Proj(proj='utm', zone=31, ellps='WGS84')
# 【方法三】EPSG
p = pyproj.Proj(init='epsg:32631')
```

# 同基准下的转换
## 地理坐标<->投影坐标
```python
import pyproj
utm_proj = pyproj.Proj('+proj=utm +zone=31 +ellps=WGS84') #定义投影
x,y = utm_proj(2.294694, 48.858093) #地理坐标-->投影坐标
	# utm_proj中的x,y可以是一个坐标对，而返回值也是两个列表
x1,y1 = utm_proj(x, y, inverse=True) #投影坐标-->地理坐标：会有一点舍入精度误差
```

# 不同基准下的转换
## 投影坐标的转换
```python
wgs84 = pyproj.Proj('+proj=utm +zone=18 +datum=WGS84')
nad27 = pyproj.Proj('+proj=utm +zone=18 +datum=NAD27')
x,y = pyproj.transform(wgs84, nad27, 580744.32, 4504695.26) #转换
```

# 大圆距离


## 计算大圆距离
【大圆距离】地球上两个点之间的最短距离（考虑曲率的情况下）

```python
# 【例子】洛杉矶->柏林的大圆距离
la_lat, la_lon = 34.0500, -118.2500
berlin_lat, berlin_lon = 52.5167, 13.3833
geod = pyproj.Geod(ellps='WGS84') #使用椭圆体来实例化一个Geod对象
forward, back, dist = geod.inv(la_lon, la_lat, berlin_lon, berlin_lat)
# 【结果】
# forward: 27.2328
# back: -38.4914
# dist: 9331934.8781
# 【意义】
# 1. 从洛杉矶以27.2328的角度走9331934.8781米，即可到达柏林
# 2. 从柏林以-38.4915的方位，走9331934.8781米，即可到达洛杉矶
```

## 计算朝某方位往前走某距离到达的位置
```python
x, y, bearing = geod.fwd(berlin_lon, berlin_lat, back, dist)
# 【意义】
# x，y：到达的位置
# bearing： 终点->柏林 的方位角
```

## 计算起终点之间等间距的点集
```python
coords = geod.npts(lat_lon, lat_lat, berlin_lon, berlin_lat, 100)
```