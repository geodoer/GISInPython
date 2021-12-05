# -*- encoding:utf-8 -*-
import os
import sys
import arcpy
from arcpy import env

workspace = r'F:\landsat8' #文件
outpath = r'D:\layer_stacking' #结果存放

# function:按顺序拼接字符串
def getInputParam(files):
    ret = ""
    for i in range(1,12): #11个波段
        judge = "B%d.TIF" % i
        for file in files: #拼接1-11波段
            if judge in file:
                print file
                ret = ret + file + ";"
                files.remove(file) #去除
                break
    for file in files:  # 拼接其他的
        print file
        ret = ret + file + ";"
    ret = ret[:-1] #去除最后的;
    return ret

dirs = os.listdir(workspace)
for dir in dirs:
    files_path = os.path.join(workspace,dir)
    files = os.listdir(files_path)
    input_param = getInputParam(files)
    env.workspace = files_path
    outpath = os.path.join(outpath,dir + ".tif")
    arcpy.CompositeBands_management(input_param, outpath)
