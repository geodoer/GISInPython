# -*- coding:utf-8 -*-

import sys,arcpy
import arcgisscripting,os
import random

fileout = r'C:\Users\PasserQi\Desktop\testWGS84\p.shp'


if __name__ == '__main__':
    # ------------------------------------
    # 保存成shp文件
    gp = arcgisscripting.create()
    # 创建shp文件
    outWorkspace = os.path.split(fileout)[0]
    outName = os.path.split(fileout)[-1]
    spat_ref = "4326"
    gp.CreateFeatureClass_management(outWorkspace, outName, "POLYGON", "", "", "", spat_ref)
    # 获取fileout文件的游标，插入数据
    cur = gp.InsertCursor(fileout)
    # 新的一行
    newRow = cur.newRow()
    # 插入数据
    XYarray = gp.CreateObject("array")
    point = gp.CreateObject("point")
    # 左下角点
    point.X = 21.5351908044064
    point.Y = 115.14078044129295
    XYarray.add(point)
    # 左上角
    point.X = 25.667828936874372
    point.Y = 115.14050321000144
    XYarray.add(point)
    # 右上角
    point.X = 25.668052170553292
    point.Y = 119.6505050275246
    XYarray.add(point)
    # 右下角
    point.X = 21.535430985538962
    point.Y = 119.65078072927248
    XYarray.add(point)
    # 左下角点
    point.X = 21.5351908044064
    point.Y = 115.14078044129295
    XYarray.add(point)

    newRow.setValue("Shape",XYarray) #实体的形状，面状一定要闭合的点
    cur.InsertRow(newRow) #新的一行
    del cur,newRow
