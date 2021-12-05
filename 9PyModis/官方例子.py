# coding:utf8
import os
import glob
from pymodis import downmodis


dest = r"D:\mycode\GISandPython\2PyModis\download" # 目标文件夹
tiles = "h18v04,h19v04" # 下载的瓦片
day = "2014-08-14"      #开始时间
delta = 1               #下载天数


files = []

# ---------------- 下载
def download():
    # 此时，我们可以初始化downmodis对象。我们将在“/tmp”目录下下载MODIS LST产品
    modisDown = downmodis.downModis(
        destinationFolder=dest,
        password="MiMa12345",
        user="glyun",
        tiles=tiles,
        today=day,
        delta=delta
    )
    modisDown.connect() #此时，我们开始下载文件。

    modisDown.downloadsAllDay()
    files = glob.glob(os.path.join(dest, 'MOD11A1.A2014*.hdf'))
    print(files)


# ---------------- 解析
from pymodis import parsemodis
def param():
    modisParse = parsemodis.parseModis(files[0])
    modisParse.retBoundary()
    modisParse.retMeasure()

    # ---------------- 解析多个文件
    modisMultiParse = parsemodis.parseModisMulti(files)
    # 获得边界
    modisMultiParse.valBound()
    modisMultiParse.boundary
    # 为拼接的文件写XML
    modisMultiParse.writexml(os.path.join(dest, 'modismultiparse.xml'))
    # 打印创建的XML文件
    f = open(os.path.join(dest, 'modismultiparse.xml'))
    lines = f.readlines()
    p = [l.strip() for l in lines]
    f.close()
    print( "\n".join(p) )

# ---------------- 创建拼接文件
# 使用GDAL库创建mosaic
# 使用子集 白天温度、晚上温度、它的质量层
from pymodis.convertmodis_gdal import createMosaicGDAL
def mosaic():
    # [daily temp, quality for daily, not used, not used, nightly temp, quality for nightly]
    subset = [1,1,0,0,1,1]
    output_pref = os.path.join(dest, 'MOD11A1.A2014226.mosaic')
    output_tif = os.path.join(dest, 'MOD11A1.A2014226.mosaic.tif')
    # 初始化对象
    mosaic = createMosaicGDAL(files, subset, 'GTiff')
    mosaic.run(output_tif)
    mosaic.write_vrt(output_pref)

# ---------------- 转换数据
from pymodis.convertmodis_gdal import convertModisGDAL
def convert():
    subset = [1, 1, 0, 0, 1, 1]

    output_pref = os.path.join(dest, 'MOD11A1.A2014226.h18v04')
    convertsingle = convertModisGDAL(hdfname=files[0], prefix=output_pref, subset=subset, res=1000, epsg=3035)
    convertsingle.run()

    # 转换后的VRT文件
    vrtfiles = glob.glob(os.path.join(dest, 'MOD11A1.A2014*.vrt'))
    print( vrtfiles )
    for f in vrtfiles:
        base = os.path.basename(f).replace('.vrt', '_vrt')
        output = os.path.join(dest, base)
        convertsingle = convertModisGDAL(hdfname=f, prefix=output, subset= [1,1,1,1], res=1000, epsg=3035, vrt=True)
        convertsingle.run_vrt_separated()

download()