# -*- coding:utf-8 -*-
# Author: PasserQi
# Time: 2017/12/18
# Func: 去边处理
# Desc: 从左边向右，从右边向左开始搜索，将边界像素替换成NoData，只会替换到边界的像素，不会替换到内部像元
# Attention: 若要打包成ArcGIS自定义工具，此文件下不能有中文
import arcpy,sys
from arcpy.sa import *

arcpy.CheckOutExtension("sptial") #权限检查
# 得到初始参数
# rasterPath = sys.argv[1]
# outPath = sys.argv[2]
# BORDER_VALUE = sys.argv[3]
#
rasterPath = r'E:\user\Desktop\DeleteDarkSide\Data\Kejicheng0.TIF' #输入栅格
outPath = r'E:\user\Desktop\DeleteDarkSide\Data\q' #输出栅格
BORDER_VALUE = 0 #边界值

if __name__ == '__main__':
    r = Raster(rasterPath) #打开栅格
    noDataValue = r.noDataValue #获取栅格中的NoData值
    array = arcpy.RasterToNumPyArray(r) #转成Numpy方便对每个像元进行处理
    bandNum,rowNum,colNum = array.shape #波段、行数、列数

    # 左边
    for i in range(0,rowNum):
        for j in range(0,colNum):
            if array[0][i][j]==BORDER_VALUE: #找到边界
                for w in range(0,bandNum):
                    array[w][i][j] = noDataValue #赋值
                print "替换:%d %d" % (i,j)
                continue
            elif array[0][i][j]==noDataValue: #是无值
                continue
            else: #是普通像素
                break #退出该行
    # 右
    for i in range(0,rowNum):
        for z in range(0,colNum):
            j = colNum - 1 - z
            if array[0][i][j]==BORDER_VALUE: #找到边界
                for w in range(0,bandNum):
                    array[w][i][j] = noDataValue  # 赋值
                print "替换:%d %d" % (i, j)
                continue
            elif array[0][i][j]==noDataValue: #是无值
                continue
            else: #是普通像素
                break #退出该行

    #保存栅格
    lowerLeft = arcpy.Point(r.extent.XMin, r.extent.YMin) #左下角点坐标
    cellWidth = r.meanCellWidth #栅格宽度
    cellHeight = r.meanCellHeight
    newRaster = arcpy.NumPyArrayToRaster(array,lowerLeft,cellWidth,cellHeight,noDataValue) #转换成栅格
    newRaster.save(outPath) #保存