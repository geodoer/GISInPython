# https://zhuanlan.zhihu.com/p/397158219

# 点转线
from shapely.geometry import LineString,Point,Polygon 
def point_to_line(df): 
    return LineString(df.sort_values("number")[["x","y"]].values) 

# 点转面
from shapely.geometry import LineString,Point,Polygon 
def point_to_line(df): 
     return Polygon(LineString(df.sort_values("number")[["x","y"]].values))

# 面转线
