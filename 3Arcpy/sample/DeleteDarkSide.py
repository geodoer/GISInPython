# -*- coding:utf-8 -*-
# Author: PasserQi
# Time: 2017/12/18
# Func: 去边处理
# Desc: 从四个角开始搜索，将边界像素替换成NoData，只会替换到边界的像素，不会替换到内部像元
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
outPath = r'E:\user\Desktop\DeleteDarkSide\Data\quheibian' #输出栅格
BORDER_VALUE = 0 #边界值



directions = [ [-1,0], [1,0], [0,-1], [0,1] ] #搜索方向数组：上 下 左 右
def bfs(q):
    # bfs
    while len(q) != 0:
        x, y = q.pop()
        # 处理x,y
        for i1 in range(0, bandNum):
            array[i1][x][y] = noDataValue
        for dir in directions:  # x,y的相邻顶点
            i = x + dir[0]
            j = y + dir[1]
            if i < 0 or j < 0 or i >= rowNum or j >= colNum:  # 出界
                continue
            elif array[0][i][j] == noDataValue:  # 访问过
                continue
            elif array[0][i][j] != BORDER_VALUE or array[1][i][j] != BORDER_VALUE or array[2][i][j] != BORDER_VALUE:  # 有值，即边界
                continue
            elif array[0][i][j] == BORDER_VALUE and array[1][i][j] == BORDER_VALUE and array[2][i][j] == BORDER_VALUE:  # 无值
                print "替换值：%d %d" % (i, j)
                q.append([i, j])

if __name__ == '__main__':
    r = Raster(rasterPath) #打开栅格
    noDataValue = r.noDataValue #获取栅格中的NoData值
    print noDataValue
    array = arcpy.RasterToNumPyArray(r) #转成Numpy方便对每个像元进行处理
    bandNum,rowNum,colNum = array.shape #波段、行数、列数

    #寻找起始点
    q = []
    # 左上角
    Flag = False
    for i in range(0,rowNum/2):
        for j in range(0,colNum):
            if array[0][i][j]==BORDER_VALUE: #找到边界
                Flag = True
                q.append([i,j])
                break
            elif array[0][i][j]==noDataValue: #是无值
                continue
            else: #是普通像素
                break #退出该行
        if Flag:
            break
    print q
    bfs(q)
    # 右上角
    Flag = False
    for i in range(0,rowNum/2):
        for z in range(0,colNum):
            j = colNum - 1 - z
            if array[0][i][j]==BORDER_VALUE: #找到边界
                Flag = True
                q.append([i,j])
                break
            elif array[0][i][j]==noDataValue: #是无值
                continue
            else: #是普通像素
                break #退出该行
        if Flag:
            break
    print q
    bfs(q)
    # 左下角
    Flag = False
    for z in range(0, rowNum/2):
        i = rowNum - 1 - z
        for j in range(0, colNum):
            if array[0][i][j] == BORDER_VALUE:  # 找到边界
                Flag = True
                q.append([i, j])
                break
            elif array[0][i][j] == noDataValue:  # 是无值
                continue
            else:  # 是普通像素
                break  # 退出该行
        if Flag:
            break
    print q
    bfs(q)
    # 右下角
    Flag = False
    for z in range(0, rowNum/2):
        i = rowNum - 1 - z
        for w in range(0, colNum):
            j = colNum - 1 - w
            if array[0][i][j] == BORDER_VALUE:  # 找到边界
                Flag = True
                q.append([i, j])
                break
            elif array[0][i][j] == noDataValue:  # 是无值
                continue
            else:  # 是普通像素
                break  # 退出该行
        if Flag:
            break
    print q
    bfs(q)


    #保存栅格
    lowerLeft = arcpy.Point(r.extent.XMin, r.extent.YMin) #左下角点坐标
    cellWidth = r.meanCellWidth #栅格宽度
    cellHeight = r.meanCellHeight
    newRaster = arcpy.NumPyArrayToRaster(array,lowerLeft,cellWidth,cellHeight,noDataValue) #转换成栅格
    newRaster.save(outPath) #保存