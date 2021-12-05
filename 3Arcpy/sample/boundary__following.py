# -*- coding:utf-8 -*-
# Author: PasserQi
# Time: 2017/12/19
# Func: 提取出遥感图像的边界
# Desc: 使用边界跟踪算法，此实例使用八连通邻域，输入的边界为
import arcpy,sys,threading
from arcpy.sa import *

rasterPath = r'E:\user\Desktop\[ArcPy] 去除遥感影像黑边\Data\Kejicheng0.TIF' #输入栅格
outPath = r'E:\user\Desktop\DeleteDarkSide\Data\q' #输出栅格
BORDER_VALUE = 0 #边界值

directions = [ [0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1],[1,0],[1,1]] #方向数组
def following(dir,boundary): #内边界
    start_i,start_j = boundary[0] #找出第一个
    x,y = boundary[-1] #找出最后一个

    # print boundary[0] + boundary[-1]

    if len(boundary)!=1 and start_i==x and start_j==y: #闭合了
        return

    x = x + directions[dir][0] #移动
    y = y + directions[dir][1] #移动
    flag = False #标识是否找到下一个边界
    if x<0 or y<0 or x>=rowNum or y>=colNum: #出边界
        flag = False #没有找到，继续找
    elif array[0][x][y]!=BORDER_VALUE and array[0][x][y]!=noDataValue: #有像素
        flag = True
        boundary.append([x,y] )
        if x==start_i and y==start_j:
            return

    #没有找到下一个继续搜索
    if flag==True: #找到了下一个边界像素
        if dir%2==0:
            dir = (dir+7)%8
        else:
            dir = (dir+6)%8
    else: #未找到
        dir = (dir+1)%7

    print len(boundary)
    following(dir,boundary)


if __name__ == '__main__':
    sys.setrecursionlimit(1000000)  # 例如这里设置为一百万

    r = Raster(rasterPath) #打开栅格
    noDataValue = r.noDataValue #获取栅格中的NoData值
    array = arcpy.RasterToNumPyArray(r) #转成Numpy方便对每个像元进行处理
    bandNum,rowNum,colNum = array.shape #波段、行数、列数

    # 找出图像最左上方的像素
    flag = False
    for i in range(0,rowNum):
        for j in range(0,colNum):
            if array[0][i][j]!=BORDER_VALUE and array[0][i][j]!=noDataValue:
                start_i = i
                start_j = j
                flag = True
                break
        if flag:
            break
    boundary = [] #边界数组
    boundary.append([start_i,start_j] )
    print boundary

    # 开始搜索
    dir = 7 #起始搜索方向

    threading.stack_size(200000000) #堆大小设置
    thread = threading.Thread(target=following(dir,boundary))
    thread.start()

