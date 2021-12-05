# Author:PasserQi
# Time:2017/11/24
# Desc:Raster 2001 equally reclass from min to max


import arcpy,sys
from arcpy.sa import *

arcpy.CheckOutExtension("sptial") # check license

# --------------------------
# get param
rasterPath = sys.argv[1] # the path of raster 2001
outPath = sys.argv[2] # the path of the resulting raster 2001
startingNum = int(sys.argv[3]) # the starting num of reclassing
groupCnt = int(sys.argv[4]) # the number of the group

# test param
# rasterPath = r'E:\user\Desktop\test\slope' # the path of raster 2001
# outPath = r'E:\user\Desktop\test\reclass_tmp' # the path of the resulting raster 2001
# startingNum = 1 # the starting num of reclassing
# groupCnt = 10 # the number of the group

# --------------------------
# processing

r = Raster(rasterPath) # open the raster

# calcuate
max = r.maximum # get the maximum of this raster
min = r.minimum # get the minimum of this raster
d = (max - min)/groupCnt # the distance


array = arcpy.RasterToNumPyArray(r) # the Raster to NumPy
rowNum,colNum = array.shape
for i in range(0,rowNum):
    for j in range(0,colNum):
        value = array[i][j]
        if value==max: # the value of max is specific
            array[i][j] = groupCnt + startingNum - 1
            continue
        cnt = groupCnt - 1
        while cnt!=-1:
            if value >= min+d*cnt:
                array[i][j] = cnt + 1
                break
            cnt=cnt-1

# save raster from numpy
lowerLeft = arcpy.Point(r.extent.XMin, r.extent.YMin)
cellSize = r.meanCellWidth
newRaster = arcpy.NumPyArrayToRaster(array,lowerLeft,cellSize)
newRaster.save(outPath)