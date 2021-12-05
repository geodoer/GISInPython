# coding:utf-8
def excel_to_shp(in_path, lon='lon', lat='lat', in_espg=4326, out_espg=4326):
    ''' Excel文件转成点状shp
    :param path:        Excel路径
    :param lon:         Longitude所在字段
    :param lat:         Latitude所在字段
    :param in_espg:     in_path的坐标系
    :param out_espg:    out_path的坐标系（即保存的坐标系）
    :return:
    '''
    import geopandas, os
    import pandas as pd
    (fn, ext) = os.path.splitext(in_path)
    out_path = in_path.replace(ext, '')

    df = pd.read_excel(in_path, 0)  # 打开第一个sheet
    gdf = geopandas.GeoDataFrame(
        df,
        geometry=geopandas.points_from_xy(df[lon], df[lat])
    )
    gdf.crs = {
        'init' :'epsg:{}'.format(in_espg)
    }
    if in_espg!=out_espg: #转坐标
        gdf = gdf.to_crs({'init': 'epsg:{}'.format(out_espg)} )
    gdf.to_file(out_path, encoding="utf-8")

if __name__ == '__main__':
    path = r'C:\Users\PasserQi\Desktop\厦门社区.xls'
    excel_to_shp(path, lon='x', lat='y', in_espg=4326, out_espg=3395)