# -*- coding: utf-8 -*-
# @Time    : 2019/4/12 8:03
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : shptotxt
# @Software: PyCharm
# @Version :
# @Desc    : 将shp中的geometry输出到txt中

import sys
from osgeo import ogr

def usage():
    print("=============================================")
    print("Help menu")
    print("[func] shapefile to txt")
    print("[desc] only output one attribute(can be specified)")
    print("[format] attr_value:x1,y1 x2,y2 x3,y3 ")
    print("shptotxt.exe -i D:\\tmp\\input.shp -o out.txt")
    print("params       description                        exmaple")
    print("-h           get help                           -h")
    print("-i           input file path                    -i D:\\tmp\input.shp")
    print("-o           save file path                     -o D:\\tmp\out.txt")
    print("-attrindex   attribute index(starting from 0)   -attrindex 0")


# ================================================
#
# Program mainline
#
def main(argv=None):
    # params
    input_file = ""
    out_file = "out.txt"
    attr_index = 0

    if argv is None:
        argv = sys.argv
    argv = ogr.GeneralCmdLineProcessor( argv )
    print("[get agv] {}".format(argv) )
    if argv is None:
        sys.exit(0)

    # parse command line arguments
    i = 1
    while i < len(argv):
        arg = argv[i]

        if arg == '-i':
            i = i+1
            input_file = argv[i]
        elif arg == '-o':
            i = i+1
            out_file = argv[i]
        elif arg == '-attrindex':
            i = i+1
            attr_index = argv[i]
            attr_index = int(attr_index)
        elif arg == '-h':
            usage()
            sys.exit(1)
        elif arg[:1] == '-':
            print("[parameter error] parameter unrecognized:{}".format(arg) )
            usage()
            sys.exit(1)
        i = i+1

    shp_to_txt(input_file, out_file, attr_index)

def shp_to_txt(input_file, out_file, attr_index):
    ds = ogr.Open(input_file)
    if ds is None:
        print("[input_file error] {}".format(input_file))
        sys.exit(1)

    layer = ds.GetLayer(0)
    if layer is None:
        print("[layer error] check out the shape file")
        sys.exit(1)

    geom_type = ""
    out_str = ""
    feat = layer.GetNextFeature()
    # 获取属性名
    attrs = feat.keys()
    length = len(attrs)
    if attr_index >= length:
        print("[attrindex error] index out of bounds")
        print("[attribute list] attribute_length={}\tattrindex={}".format(length, attr_index)  )
        print("index\tattrname")
        i = 0
        for key in attrs:
            print("{}\t{}".format(i, key) )
            i += 1
        sys.exit(1)
    attrname = attrs[attr_index]
    while feat:
        # get attribute
        out_str += "{}:".format(
            feat.GetField(attrname)
        )
        geom = feat.geometry()
        # get geometry
        if geom.GetGeometryType() == ogr.wkbPolygon:
            geom_type = "wkbPolygon"
            ring = geom.GetGeometryRef(0)
            for i in range(ring.GetPointCount()):
                out_str += "{},{} ".format(
                    ring.GetX(i),
                    ring.GetY(i)
                )
        elif geom.GetGeometryType() == ogr.wkbLineString:
            geom_type = "wkbLineString"
            # line
            for i in range(geom.GetPointCount()):
                out_str += "{},{} ".format(
                    geom.GetX(i),
                    geom.GetY(i)
                )
        elif geom.GetGeometryType() == ogr.wkbPoint:
            geom_type = "wkbPoint"
            # point
            out_str += "{},{} ".format(
                geom.GetX(),
                geom.GetY()
            )
        else:
            print("[ERROR] the geometry type of shape file can not suppost. currentlly only suppost wkbPoint, wkbLineString and wkbPolygon")
            sys.exit(1)

        feat = layer.GetNextFeature()
        out_str += '\n'

    with open(out_file, "w") as fp:
        fp.write(out_str)

    print("[done] the geometry type of this shape file is {}".format(geom_type))
    print('[done] {}'.format(out_file))

if __name__ == '__main__':
    sys.exit(main() )

    # input_file = r"D:\mycode\GISandPython\9data\park_polygon_shp\park_polygon.shp" #polygon --> ok
    # input_file = r"D:\mycode\GISandPython\9data\park_point_shp\xiamen_20181128_park.shp" #point --> ok
    # input_file = r'D:\mycode\GISandPython\9data\road_shp\xiamen_20181116_road.shp' #line --> ok
    # input_file = r'D:\mycode\GISandPython\1.1ORG\example\shptotxt\tmp\zhanwei.shp'
    # out_file = "out.txt"
    # attr_index = 1
    # shp_to_txt(input_file, out_file, attr_index)