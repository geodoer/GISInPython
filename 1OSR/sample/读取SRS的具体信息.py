from osgeo import ogr

datasource = ogr.Open(r'E:\data\US\states_48.shp')

layer = datasource.GetLayer()

srs = layer.GetSpatialRef()
print(srs)
srs.IsProjected()
srs.GetAttrValue('PROJCS') is None
srs.GetAttrValue('AUTHORITY')
srs.GetAttrValue('AUTHORITY', 1)
srs.GetAuthorityCode('DATUM')

from osgeo import osr
srs.GetProjParm(osr.SRS_PP_FALSE_EASTING)

srs.GetProjParm(osr.SRS_PP_FALSE_EASTING)