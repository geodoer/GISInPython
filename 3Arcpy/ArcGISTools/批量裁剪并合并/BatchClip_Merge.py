# -*- coding: utf-8 -*-



import os
import re
import arcpy
import shutil


def get_files(in_dir, condition_re="", extension=""):
    ret = []
    for file in os.listdir(in_dir):
        if extension!="":
            if not file.endswith(extension):
                continue
        if condition_re!="":
            if not re.match(condition_re, file):
                continue

        fp = os.path.join(in_dir, file)
        ret.append(fp)
    return ret



if __name__ == '__main__':


    in_dir          = arcpy.GetParameterAsText(0)  
    clip_features   = arcpy.GetParameterAsText(1)   
    out_file        = arcpy.GetParameterAsText(2)   
    condition_re    = arcpy.GetParameterAsText(3) 
    extension       = arcpy.GetParameterAsText(4)

    print("[Step] Get input file")
    files = get_files(in_dir, condition_re, extension)

    print("[Step] Clip")
    clip_list = []

    out_dir = os.path.dirname(out_file)
    tmp_dir = os.path.join(out_dir, "tmp")
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    cnt = 1
    for file in files:
        in_features = file
        out_feature_class = os.path.join(tmp_dir, "clip{}.shp".format(cnt) )
        cnt +=1
        arcpy.Clip_analysis(in_features, clip_features, out_feature_class)
        clip_list.append(out_feature_class)
        print("\t[done] {}".format(file) )
    print("done")

    print("[Step] Merge")
    arcpy.Merge_management(clip_list, out_file)
    print("done")

    print("[Step] Delete temporary files")
    shutil.rmtree(tmp_dir)
