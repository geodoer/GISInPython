# -*- encoding: utf-8 -*-
"""
@File    : 汇总学校周围的居民区.py
@Time    : 2020/1/14 15:17
@Author  : GeoDoer
@Email   : geodoer@163.com
@Software: PyCharm
@Func    : 统计厦门校园体育场附近的商务住宅
@Desc    :
"""

import geopandas
import os

out_dir = r"C:\Users\PasserQi\Desktop\xm_map\统计结果"
bufpnt_fp = r"C:\Users\PasserQi\Desktop\xm_map\xm\体育\厦门校园体育场.shp"
stat_fp = r"C:\Users\PasserQi\Desktop\xm_map\xm\厦门商务住宅\厦门商务住宅.shp"
dis = 4000 #1500 4000

# 图层缓冲区
def LayerBuffer(gdf, dis):
    old_crs = gdf.crs
    gdf = gdf.to_crs('+init=epsg:3395') #转换为WGS4 UTM Zone 50N 投影坐标系
    gdf['geometry'] = gdf.buffer(dis)   #buffer操作
    gdf = gdf.to_crs(old_crs)   #再转回来
    return gdf


def main(bufpnt_fp, stat_fp, dis):
    # read
    bufpnt_gdf = geopandas.read_file(bufpnt_fp)
    stat_gdf = geopandas.read_file(stat_fp)

    # buffer
    buf_gdf = LayerBuffer(bufpnt_gdf, dis)

    # sjoin
    right_gdf = geopandas.sjoin(buf_gdf, stat_gdf, how="right", op='intersects')

    # 统计数量、合并名称
    nums = []
    names = []
    for i in range(0, len(buf_gdf) ):
        name = buf_gdf.iloc[i]["schoolname"]   #取出学校姓名
        name_gdf = right_gdf.loc[ right_gdf["schoolname"] == name]  #获取该学校姓名的行
        nums.append( len(name_gdf) ) #计算个数
        # 统计姓名
        str = ""
        for index, row in name_gdf.iterrows():
            str += "{};".format(row["name"] )
        names.append(str)
    buf_gdf["nums"] = nums
    buf_gdf["names"] = names

    # save
    # buf_gdf.to_file(r"{}\{}".format( out_dir, "缓冲区图层的结果.shp"), encoding="utf-8")
    buf_gdf.to_excel(r"{}\{}".format( out_dir, "缓冲区图层的结果.xlsx") , encoding="utf-8")

    # right_gdf.to_file(r"{}\{}".format( out_dir, "统计图层的结果.shp" ) , encoding="utf-8")
    # right_gdf.to_excel(r"{}\{}".format(out_dir, "统计图层的结果.xlsx"), encoding="utf-8")



if __name__ == '__main__':
    main(bufpnt_fp, stat_fp, dis)
    pass




