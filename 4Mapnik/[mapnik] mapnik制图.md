# mapnik
【详细介绍】https://blog.csdn.net/summer_dew/article/details/86608111#mapnik_34
【安装】

## 建立地图对象
```python
# 【导入Python绑定】
import mapnik2 as mapnik

# 【建立mapnik对象】
m = mapnik.Map(6000, 3000, "+proj=latlong +datum=WGS84") #指定宽度、高度
m.background = mapnik.Color('steeblue') #设置背景的颜色为steelblue
```

## 创建样式
```python
# 【创建样式】
## 地图对象的样式
s = mapnik.Style() 
	### 地图对象的规则
	r = mapnik.Rule() 
		#### 多边形要素的符号
		polygon_symbolizer = mapnik.PolygonSymbolizer(mapnik.Color('#f2eff9') ) 
		r.symbols.append(polygon_symbolizer) #将符号添加到规则中
		#### 线状多边形要素的符号
		line_symbolizer = mapnik.LineSymbolizer(mapnik.Color('rgb(50%,50%,50%)'),0.1 ) 
		r.symbols.append(line_symbolizer) #符号添加到规则中
	s.rules.append(r) #将规则添加到样式中
m.append_style('My Style',s) #将样式添加到地图中
```

## 创建数据源
【数据源】创建样式时，需要一个**世界边界的样本面的shapefile**。要用python将转换成一个mapnik数据源

```python
ds = mapnik.Shapefile(file='/gdata/world_borders.shp')
```

## 创建图层
```python
layer = mapnik.Layer('world') #创建图层
layer.datasource = ds #设置图层的数据源
layer.styles.append('My Style') #设置图层的样式
```

## 地图渲染
```python
m.layers.append(layer) #把图层加到地图里
m.zoom_all() #显示图层的全部范围（如果不把图层全部显示，那么输出很可能是空白的）
mapnik.render_to_file(m, 'xworld.png', 'png') #渲染地图，把数据写成png格式->然后保存到当前目录world.png
```