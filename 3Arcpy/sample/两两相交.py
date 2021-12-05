# -*- coding: utf-8 -*-
# @Time    : 2019/6/7 8:07
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : 两两相交
# @Software: PyCharm
# @Version :
# @Desc    :

import os
import arcpy

dir1 = r""
dir2 = r""
output = r""

# 遍历第一个文件夹
for root1,dis1,files1 in os.walk(dir1):
    # 遍历root文件夹下的files
    for file1 in files1:
        if file1.endswith(".shp"): #找到shp文件
            print "===== [doing] {} =====".format(file1) #第一个文件
            # 遍历第二个文件夹
            for root2,dis2,files2 in os.walk(dir2):
                for file2 in files2:
                    if file2.endswith(".shp"):
                        # file1与file2相交，并输出到fp
                        file1_path = os.path.join(root1, file1)
                        file2_path = os.path.join(root2, file2)

                        fn = "{}_{}_sect.shp".format(file1[0:2], file2[0:2])
                        fp = os.path.join(output, fn)

                        print "{} 与 {} 相交，输出至{}".format(file1_path, file2_path, fp)
                        # 相交语句
