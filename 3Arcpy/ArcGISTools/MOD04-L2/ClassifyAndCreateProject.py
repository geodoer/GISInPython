# -*- coding: utf-8 -*-
# @Time    : 2019/8/6 16:38
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : ClassifyAndCreateProject
# @Software: PyCharm
# @Version :
# @Desc    :
#       1. classify multiple batches of data in same folder
#       2. create MOD04-L2 project in output folder

import sys
import os
import arcpy

# arcpy param
# input_dir = r"D:\mycode\GISandPython\2Arcpy\ArcGISTools\MOD04-L2\MOD04-L2_data"
# project_dir = r"D:\mycode\GISandPython\2Arcpy\ArcGISTools\MOD04-L2\project"
input_dir = sys.argv[1]
project_dir = sys.argv[2]

# project param
categorys = {
}

def classify(input_dir):
    fns = os.listdir(input_dir)
    if len(fns)==0:
        arcpy.AddMessage("[ERROR]\tCan't fine files in {}.".format(input_dir) )
    else:
        arcpy.AddMessage("[OK]\tFine {} files.".format( len(fns) ) )

    for fn in fns:
        category_name = fn.split('.')[1]
        # create dir
        if category_name not in categorys:
            categorys[category_name] = create_dir(category_name)
        # copy files
        data_dir = categorys[category_name]["Data"]
        srcfp = os.path.join(input_dir, fn)
        dstfp = os.path.join(data_dir, fn)
        copyfile(srcfp, dstfp)

    arcpy.AddMessage("[OK]\t" + project_dir)
    pass

def create_dir(category_name):
    ret = {
        "Data" : None,
        "Subset" : None,
        "DefineSRS" : None,
        "Projection" : None,
    }
    # category dir
    category_dir = os.path.join(project_dir, category_name)
    mkdir(category_dir)
    # create dir in category dir
    for dirname in ret.keys():
        if ret[dirname]==None:
            ret[dirname] = os.path.join(category_dir, dirname)
            mkdir( ret[dirname] )
    return ret

def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    if not os.path.exists(path):
        os.mkdir(path)
        arcpy.AddMessage("[OK] Create Dir:{}".format(path) )
        return True


def copyfile(srcfile,dstfile):
    import shutil
    if not os.path.isfile(srcfile):
        arcpy.AddMessage("[ERROR]\t%s not exist!"%(srcfile) )
    else:
        fpath,fname=os.path.split(dstfile)
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        shutil.copyfile(srcfile,dstfile)
        arcpy.AddMessage("[OK] copy %s -> %s"%(srcfile, dstfile) )

if __name__ == '__main__':
    classify(input_dir)

    pass