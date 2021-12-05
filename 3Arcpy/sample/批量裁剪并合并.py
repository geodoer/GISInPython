# -*- coding: utf-8 -*-
# @Time    : 2019/4/14 20:15
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : 批量裁剪并合并
# @Software: PyCharm
# @Version :
# @Desc    :


import os
import re
import arcpy
import shutil


def get_files(in_dir, condition_re="", extension=""):
    ret = []
    for file in os.listdir(in_dir):
        # 后缀名过滤
        if extension!="":
            if not file.endswith(extension):
                continue
        # re条件筛选
        if condition_re!="":
            if not re.match(condition_re, file):
                continue

        fp = os.path.join(in_dir, file)
        ret.append(fp)
    return ret



if __name__ == '__main__':
    # in_dir = r"E:\SAR\ps\geocoding"     #输入文件夹
    # condition_re = ".*PS.*"             #re筛选
    # extension = ".shp"                  #扩展名
    # clip_features = r'E:\SAR\ps\xiamen.shp' #裁剪的shp
    # out_file = r"E:\SAR\tmp\xiamen_ps.shp"  #输出文件

    in_dir          = arcpy.GetParameterAsText(0)   #输入文件夹
    clip_features   = arcpy.GetParameterAsText(1)   #裁剪的shp
    out_file        = arcpy.GetParameterAsText(2)   #输出文件
    condition_re    = arcpy.GetParameterAsText(3)   # re筛选
    extension       = arcpy.GetParameterAsText(4)   # 扩展名

    print("[Step] Get input file")
    files = get_files(in_dir, condition_re, extension)

    # 裁剪
    print("[Step] Clip")
    clip_list = []

    out_dir = os.path.dirname(out_file)
    tmp_dir = os.path.join(out_dir, "tmp")
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    cnt = 1
    for file in files:
        # 输入的文件
        in_features = file
        # 输出的文件
        out_feature_class = os.path.join(tmp_dir, "clip{}.shp".format(cnt) )
        cnt +=1
        # 裁剪
        arcpy.Clip_analysis(in_features, clip_features, out_feature_class)
        clip_list.append(out_feature_class)
        print("\t[done] {}".format(file) )
    print("done")

    # 合并
    print("[Step] Merge")
    arcpy.Merge_management(clip_list, out_file)
    print("done")

    # 删除临时文件
    print("[Step] Delete temporary files")
    shutil.rmtree(tmp_dir)  # 递归删除文件夹
