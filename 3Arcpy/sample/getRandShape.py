# -*- coding:utf-8 -*-
# Author: PasserQi
# Time:2017/12/18
# Func:将shp文件分成6*6份，每份赋予分配0-35中不同的值，输出形式为面状shp
# Desc:若要创建ArcGIS自定义工具，该文件不能出现中文
import sys,arcpy
import arcgisscripting,os
import random

#
# filein = sys.argv[1]
# fileout = sys.argv[2]
# number = sys.argv[3]
filein = r'E:\user\Desktop\RandShp\Data\road.shp'
fileout = r'E:\user\Desktop\RandShp\rand_polygon.shp'
number = 6

# @function:产生number*number个不重复的随机数，数值范围在0 <= n <= number-1
# @param: number
# @return: list
def getRandList(number):
    randList = []
    while len(randList) != number*number:
        n = random.randint(0, number*number-1) #产生随机数：0 <= n <= number-1
        if n in randList: #已经生成过了
            continue
        else:
            randList.append(n)
    return randList


if __name__ == '__main__':
    desc = arcpy.Describe(filein) #获取shp的信息
    # shp的范围
    XMin = desc.extent.XMin
    XMax = desc.extent.XMax
    YMin = desc.extent.YMin
    YMax = desc.extent.YMax
    step_x = (XMax - XMin) / number # x的步长
    step_y = (YMax - YMin) / number # y的步长

    #得到number*number个不重复的随机数
    randList =  getRandList(number)

    # ------------------------------------
    # 保存成shp文件
    gp = arcgisscripting.create()
    # 创建shp文件
    outWorkspace = os.path.split(fileout)[0]
    outName = os.path.split(fileout)[-1]
    spat_ref = desc.spatialReference
    gp.CreateFeatureClass_management(outWorkspace, outName, "POLYGON", "", "", "", spat_ref)
    # 添加字段
    gp.AddField_management(fileout, "number", "LONG")
    # 获取fileout文件的游标，插入数据
    cur = gp.InsertCursor(fileout)
    # 新的一行
    newRow = cur.newRow()
    # 插入数据
    for i in range(0,number):
        for j in range(0,number):
            XYarray = gp.CreateObject("array")
            point = gp.CreateObject("point")
            # 左下角点
            point.X = XMin + i*step_x
            point.Y = YMin + j*step_y
            XYarray.add(point)
            # 左上角
            point.X = XMin + (i + 1) * step_x
            point.Y = YMin + j * step_y
            XYarray.add(point)
            # 右上角
            point.X = XMin + (i + 1) * step_x
            point.Y = YMin + (j + 1) * step_y
            XYarray.add(point)
            # 右下角
            point.X = XMin + i * step_x
            point.Y = YMin + (j+1) * step_y
            XYarray.add(point)
            # 左下角点
            point.X = XMin + i * step_x
            point.Y = YMin + j * step_y
            XYarray.add(point)

            newRow.setValue("Shape",XYarray) #实体的形状，面状一定要闭合的点
            newRow.setValue("number",randList[i*6+j] ) #插入随机分配的值
            cur.InsertRow(newRow) #新的一行
    del cur,newRow
