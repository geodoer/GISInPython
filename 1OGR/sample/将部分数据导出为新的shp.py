# coding:utf8
# @desc:将部分数据导出为新的shp
import sys
from osgeo import ogr

"""
【背景】此例子：打开一个文件夹作为数据源，而不是使用shp文件
【原因】shapefile驱动程序的一个特点：若文件夹中的大多数文件是shapefile格式文件，每个shapefile文件会被视为一个图层（shp文件=图层）
【使用】`ds = ogr.Open(dir, 1)` 将1作为参数：在文件夹创建一个新的图层
【注释】OGR不会覆盖现有图层，所以需要检查输出的图层是否已经存在，如果存在就要删除它
"""


# 将厦门POI数据中的“商务住宅”存成另一个shp
dir = r'..\..\92001\park_point_shp' # 数据所在文件夹
key = '商务住宅'

# ----------------- 打开一个文件夹 -----------------
ds = ogr.Open(dir, 1)
if ds is None:
    sys.exit("没有打开该文件夹")
# ----------------- 打开图层 -----------------
in_layer = ds.GetLayer("xiamen_20181128_park") #打开dir文件夹下xiamen_20181128_park.shp文件
# ----------------- 新建shp（即图层） -----------------
# 创建新的数据源时，不能覆盖现有的数据源。如果你的代码可能会覆盖现有数据，那么在创建新数据之前需要删除旧数据
if ds.GetLayer("CommercialHousing"): #已经存在
    ds.DeleteLayer("CommercialHousing") #删除
out_layer = ds.CreateLayer( #创建图层
    name="CommercialHousing",  #新建的图层名称
    srs=in_layer.GetSpatialRef(), #新建图层使用的空间参考系统，默认为空（没有设置任何空间参考系统）
    geom_type=ogr.wkbPoint, #几何类型
    options  = [ # #创建选项：传递一个字符串列表（参数在OGR网站上有文档介绍）
        # 是一个图层创建时的选项列表，只适用于特定的矢量数据类型
        "ENCODING=UTF-8" #查看"驱动程序的文档"描述
    ]
)

# --- 创建一个用于存储几何要素和属性的虚拟要素，然后将其插入到图层中 ---
# 创建一个要素，需要获得要素的定义，其包含几何类型和所有属性字段的信息
#（这样创建的空要素才可以具有相同的属性字段和几何类型）
out_layer.CreateFields(in_layer.schema) # 设置值图层的属性
out_defn = out_layer.GetLayerDefn() # 获取原数据图层的定义
out_feat = ogr.Feature(out_defn) # 按照原来的定义创建Feature
for in_feat in in_layer:
    if key in in_feat.GetField('type'): #如果"type"字段中包含"商务住宅"，就复制到新图层
        geom = in_feat.geometry()
        out_feat.SetGeometry(geom) #设置geometry
        # 设置属性值
        for i in range(in_feat.GetFieldCount() ):
            value = in_feat.GetField(i)
            out_feat.SetField(i, value)
        # 将Feature插入到图层
        out_layer.CreateFeature(out_feat)

""" 删除ds变量强制关闭文件，并将所有的编辑成果写入磁盘中
【注意】删除图层变量并不会触发这个操作，必须关闭数据源才行
【备注】如果想保持数据源打开的话，可以通过图层对象或者数据源对象调用ds.SyncToDisk()
【警告】为了使你的编辑写入到磁盘中，必须关闭文件或者调用SyncToDisk函数。如果没有这么做，并且在交互环境中还打开数据源，那么你会很失望地发现创建了一个空的数据集
"""
del ds


