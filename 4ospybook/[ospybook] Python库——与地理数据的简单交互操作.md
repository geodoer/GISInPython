【书】《Python地理数据处理》[美] Chris Garrard 著 2017年7月
【文件夹介绍】本文件夹为该书的代码与数据
【书内资源下载网址】https://www.manning.com/books/geoprocessing-with-python

# ospybook介绍——Python可视化地理数据
【ospybook】为该书作者提供的一个很好用的Python库
1. 优势：可以帮助你不用打开其他软件程序，就可以可视化数据
2. 缺点：交互性差

# 安装

1. 安装包：ospybook-1.0文件夹下(下载地址：http://manning.com/garrard/?a_aid=geopy&a_bid=c3bae5be)
2. 安装，定位setup.py目录打开命令行运行`python setup.py build`
3. 再运行`python setup.py install`安装


# 查看属性
## 使用
```python
import ospybook as pb
fn = r'D:\polygon.shp'
pb.print_attributes(fn, 3, ['NAME', 'POP_MAX'] )
```


## 函数原型
```python
print_attributes(lyr_or_fn, [n], [fields], [geom], [reset] )
1. lyr_or_fn 可以是一个图层，也可以是一个数据源路径。如果是一个数据源，使用的是第一个图层
2. n 是一个可选值，用于设置输出记录数目，默认输出所有数值
3. fields 是一个可选值，用于设置输出结果中包含的属性字段列表，默认包括所有字段
4. geom是一个可选的布尔值，用于设置是否输出几何要素类型，默认为True
5. reset是一个可选的布尔值，用于设置在输出数值之前，是否重置到第一条记录，默认为true
```

# 绘制空间数据VectorPlotter
> 依赖于：matplotlib模块

## plot函数
```python
plot(self, geom_or_lyr, [symbol], [name], [kwargs])
1. geom_or_lyr 可是是一个要素对象、图层或者指向一个数据源的路径。如果是一个数据源，数据源中的第一个图层会被绘制显示
2. symbol是一个可选值，用于设置几何要素的符号样式
	- fill=False：空心多边形
	- "bo"：蓝色的圆圈
	- "rs"：正方形
	- "b-" 蓝线？
	- "r--" 虚线（每个单元是横的）
	- "g:" 虚线（每个单元是竖的）
	- edgecolor='blue' 
	- ec="read"
	- linestyle="dashed" 或者 ls="dotted"
	- linewidth=3
3. name是一个可选值，用于为数据设定名称，以便后期可以访问它
4. kwargs是一个可选值，通过关键字进行指定。kwargs经常被用作一个不确定数量的关键字参数（an indeterminate number of keyword arguments）的缩写
```
## 在Python交互环境下
```python
>>> import os
>>> os.chdir(2001) #更改工作目录
>>> from ospybook.vectorplotter import VectorPlotter
>>> vp = VectorPlotter(True) #创建一个交互式的绘图面板
>>> vp.plot('countries.shp', fill=False) #fill参数使文件用一个空心多边形表示
>>> vp.plot('places.shp', 'bo') #fill=bo：为places.shp文件所设的bo符号表示蓝色的圆圈
```

## .py文件下
```python
from ospybook.vectorplotter import VectorPlotter
vp = VectorPlotter(False) #非交互模式创建
vp.plot('countries.shp', fill=False)
vp.draw() #调用draw函数绘制
```

## 其他常用函数
```python
vp.clear() #清除
vp.zoom(-5) #缩小范围
```