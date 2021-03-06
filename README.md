python-netCDF
=============

# 用python的netCDF4库处理nc数据，并用basemap绘图，具体步骤如下：


## 1.导入所需要的库

```python
import matplotlib.pyplot as plt
plt.rc('font',family='Times New Roman',weight='normal') 
import matplotlib.cm as cm 
import matplotlib.colors 
import numpy as np 
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap 
import matplotlib as mpl 
```

## 2.读取nc数据，查看数据基本信息

```python
fn=r'C:\Users\shaoqi_i\Desktop\E_1980_GLEAM_v31a.nc'
fn_nc=Dataset(fn) 

print('The nc file info is:') 
print(fn_nc)
```

## 3.查看数据中的所有变量
```python
print("The nc file's variables are:")
print(fn_nc.variables.keys())
```
## 4.查看数据中变量E的基本信息
```python
print("E is:")
summary_E=fn_nc.variables['E']
print(summary_E) 

## 属性
print("E's attributes are:")
attributes_E=fn_nc.variables['E'].ncattrs()
print(attributes_E)

## 单位
print("E's units are:")
units_E=fn_nc.variables['E'].units
print(units_E)

## 无效值
print("E's _FillValue are:")
FillValue_E=fn_nc.variables['E']._FillValue
print(FillValue_E)

## 名称
print("E's standard_name are:")
standard_name_E=fn_nc.variables['E'].standard_name
print(standard_name_E)

```

## 5.获取变量E，查看E的行列波段号

> 显示为（366,1440,720），366代表1981年366天，1440是行号，720是列号
```python
E=fn_nc.variables['E']
print(E.shape)

## 利用numpy的mask功能将无效值-999变成-，从而不影响后面的计算和出图
E=np.ma.masked_values(E,FillValue_E)
```

## 6.计算1981年全球的总蒸发量

> axis表示按哪个坐标轴取和，366为天数，因此取0。在hdf-view里可以看到，数据的行列号是颠倒的，不是正常的全球图，因此需要矩阵转置

```python
E_year=np.transpose(np.sum(E,axis=0))
print(E_year.shape)
```

## 7.得到数据中的经度和纬度，并计算各自的最大值和最小值

```python
lat=fn_nc.variables['lat']
lat_min=np.min(lat)
lat_max=np.max(lat)

lon=fn_nc.variables['lon']
lon_min=np.min(lon)
lon_max=np.max(lon)
```

## 8.绘图

```python
## 设置画布大小和图所占位置，subplot（1,1,1）表示画一张图，类似MATLAB里的写法
plt.figure(figsize=(40,30))
plt.subplot(1,1,1)

## 设置投影类型，此处选择了两种，一种是等经纬度投影，nc数据常用；另一种是Robinson投影。
## 等经纬度投影需要设置经纬度范围，根据前面经纬度的结果取值，resolution='l'，表示分辨率为低分辨率，主要是为了大陆边界展示的时候不那么突出，可设置成'h'查看一下效果

m=Basemap(projection='cyl',llcrnrlon=lon_min,urcrnrlon=lon_max,llcrnrlat=lat_min,urcrnrlat=lat_max,resolution='l')

## Robinson投影，设置中心经纬度
m=Basemap(projection='robin',lon_0=0,lat_0=0,resolution='l')

## 根据经纬度数组产生经纬度网格，由于经纬度都是一维数组，而E_year是二维数组，需要产生相匹配的经纬度网，从而出图。
lon,lat=np.meshgrid(lon,lat)

## 将等经纬度的经纬度网格做投影转换，转换成所设定的投影
lon,lat=m(lon,lat)

## 大陆边界，python自带
m.drawcoastlines(linewidth=0.2)

## 经纬度网格线，包括起终点和间隔，以及label标注位置和大小，线宽，可以自己调整查看
m.drawparallels(np.arange(-90, 90,30), labels=[1,0,0,0], fontsize=13,linewidth=0.8)
m.drawmeridians(np.arange(-180, 180, 45), labels=[0,0,0,1], fontsize=13,linewidth=0.8)

## 颜色，jet表示红-蓝，jet_r表示颜色反向
cmap = plt.cm.jet_r
norm = matplotlib.colors.Normalize(vmin=-50, vmax=2100)

## （1）等值线图，20表示颜色分级，可改动查看效果
cf=plt.contourf(lon,lat,E_year,20,cmap=cmap,norm=norm)

## （2）灰度图，光标在图上移动时，可以显示该点的数值，但是需要对E_year做上下颠倒处理，否则图画出来是倒的
cf=m.imshow(E_year[::-1],cmap=cmap,norm=norm)

##（3）伪彩图，与等值线图相反，是渐变型
cf=plt.pcolormesh(lon,lat,E_year,cmap=cmap,norm=norm)

## 标题
plt.title("Global Actual Evaporation in 1980",fontsize=18)

## colorbar的位置(x,y)和参数设置(宽度,高度)
cax=plt.axes([0.9, 0.11, 0.018,0.77])
cbar=plt.colorbar(cf,cax=cax)

## colorbar的数字设置，direction='in'表示黑色刻度线向里，可删掉查看效果
cbar.ax.tick_params(labelsize=13, direction='in')

## colorbar的名称
font = {'family' : 'Times New Roman',   
        'weight' : 'normal',  
        'size'   : 15,  
        }
cbar.set_label(r'Evaporation (mm)',fontdict=font)
```

## 9.保存输出

```python
plt.savefig(r'C:\Users\shaoqi_i\Desktop\evaporation.tif',dpi=100)
plt.show()
```
