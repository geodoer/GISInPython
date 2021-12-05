import arcpy, sys
from arcpy.sa import *

rasterPath = r'I:\水文分析\Fujian.gdb\slope'
outpath = r'I:\水文分析\Fujian.gdb\slope_classify'

arcpy.CheckOutExtension("sptial")
r = Raster(rasterPath)

array = arcpy.RasterToNumPyArray(r)
rowNum, colNum = array.shape
for i in range(0, rowNum):
    for j in range(0, colNum):
        value = array[i][j]
        if value < 5:
            array[i][j] = 1
            continue
        elif value >= 5 and value < 8:
            array[i][j] = 2
            continue
        elif value >= 8 and value < 15:
            array[i][j] = 3
            continue
        elif value >= 15 and value <25:
            array[i][j] = 4
            continue
        elif value >=25:
            array[i][j] = 5
            continue

lowerLeft = arcpy.Point(r.extent.XMin, r.extent.YMin)
cellWidth = r.meanCellWidth
cellHeight = r.meanCellHeight
newRaster = arcpy.NumPyArrayToRaster(array, lowerLeft, cellWidth, cellHeight)
newRaster.save(outpath)