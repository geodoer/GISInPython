> 【内容介绍】
>
> 1. 将一个文件夹下的文件按照【一定的规则】分流到不同文件夹下
> 2. 对一组数据进行批量抽取子集
> 3. 对文件夹下的所有数据进行定义投影
> 4. 对文件夹下的所有数据投影到指定坐标（UTM50N）
> 5. 对文件夹下的所有栅格数据进行拼接



[TOC]

# 【第一步】按规则分流数据

【数据】MOD04_L2数据气溶胶日产品（介绍请看附录）

【需求】该文件夹下有3天的日产品，按照名字中的A2001001、A2001003、A2001006进行分流数据

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190807093753965.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)

【工具】`[1]ClassifyAndCreateProject`

【使用】

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190807100250309.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)

【结果】

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190807100303600.gif)

【工程目录介绍】

- project						创建的输出文件夹（即工程文件夹）
  - A2001001				产品日期
    - Data						原始数据文件夹
    - Subset 		           子集输出文件夹
    - DefineSRS              定义投影输出文件夹
    - Projection              投影输出文件夹
  - A2001003
    - .... 下同



# 【第二步】抽取子集并定义坐标系

【打开一个MOD04数据】发现其具有219个波段，ID号从0开始；并且没有定义投影（在头文件中可知其投影为WGS84）

【需求】按照指定的波段进行抽取（举例：抽取ID=11的波段），并且定义投影为WGS84

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190807095447498.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190807095726413.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)

【工具】`[2]SubsetAndDefineProject`

【使用】

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190807095947455.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)

【结果】

- 抽取子数据集输出在该产品集的Subset目录中![在这里插入图片描述](https://img-blog.csdnimg.cn/20190807100048795.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)

- 定义投影的结果输出在该产品集的DefineSRS中

  ![在这里插入图片描述](https://img-blog.csdnimg.cn/20190807100422755.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)

# 【第三步】批量投影

【需求】将产品集中的DefineSRS进行批量投影至WGS84_UTM_Zone_50N

【工具】`[3]Project`

![在这里插入图片描述](https://img-blog.csdnimg.cn/2019080710093541.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)

【结果】投影的结果输出在该产品集的Projection中

![在这里插入图片描述](https://img-blog.csdnimg.cn/2019080710103383.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)



# 【第四步】拼接（即ArcGIS中的镶嵌）

【需求】将Projection中的数据集进行拼接

【工具】`[4]Mosaic`

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190807101241868.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)

【结果】输出在A2001001文件夹下

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190807101808945.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)



# 【附录】MOD04产品介绍

【MOD/MYD04】MODIS Terra/Aqua Aerosol 5-Min L2，是NASA发布的Level 2级气溶胶产品，可用来获取全球海洋和陆地环境的大气气溶胶光学特性（如：光学厚度和大小分布）和质量浓度，通过查找表（LUT）反演得到反射和传输通量，以及其他质量控制和辅助参数，其空间分辨率为3km、10km，以HDF4格式提供

- 【C5版本】10km分辨率的气溶胶产品
- 【C6版本（MOD/MYD04_3K）】3km分辨率的气溶胶产品，全称MODIS Terra/Aqua Aerosol 5-Min L2 Swath 3km



【命名规则】官方例子

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190807092605254.png)



【举例】MOD04_L2.A2001001.0110.061.2017220225602.hdf

- 【MOD04_L2】产品类型（Earth Science Data Type Name），MOD04_L2是气溶胶的日产品
- 【A2001001】卫星扫过这片区域的时间（年份、月份、天数）
  - 【A】Acquisition，因为modsi卫星分上午卫星和下午卫星就分别用A和T来表示的
  - 【2001】年
  - 【001】Julian Date是一种历法计数的方法，实际上也就是代表2001年的第1天
- 【0110】卫星扫过这片区域的时间（小时和分钟），其中这个时间是UTC时间
- 【061】Collection Version，是其数据的版本号，像其前一个版本好像就是051的，也看过不少论文是做这种版本之间差异的
- 【2017220225602】数据制作的时间（包括年份、月份、天数、小时、分钟、秒）
  - 2017年，第220天，22时56分2秒制作



【相关链接】

- [MODSI气溶胶产品MOD04_L2命名规则](http://blog.sina.com.cn/s/blog_b8e25eb20102xe5p.html)
- [NASA官方解释](http://modis-atmos.gsfc.nasa.gov/MOD04_L2/index.html)
- [MOD04_3K 产品使用方の法学习](https://blog.csdn.net/u013930678/article/details/78552183)