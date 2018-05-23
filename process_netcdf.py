# -*- coding: utf-8 -*-
"""
@author: ShaoQi(BNU 17GIS Advisor: Li Jing; NUIST 13RS Advisor: Xu YongMing)
"""

############# load packages ############### 
import matplotlib.pyplot as plt 
plt.rc('font',family='Times New Roman',weight='normal')  
import matplotlib.cm as cm
import matplotlib.colors
import numpy as np
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl

############# read netCDF file ###############
fn=r'C:\Users\shaoqi_i\Desktop\E_1980_GLEAM_v31a.nc'
fn_nc=Dataset(fn)

############ file info and variables ##############
print('The nc file info is:')
print(fn_nc)

print("The nc file's variables are:")
print(fn_nc.variables.keys())  

############ variable E info ##############

##### summary #####
print("E is:")
summary_E=fn_nc.variables['E']
print(summary_E)

##### attributes #####
print("E's attributes are:")
attributes_E=fn_nc.variables['E'].ncattrs()
print(attributes_E)

##### units #####
print("E's units are:")
units_E=fn_nc.variables['E'].units
print(units_E)

##### FillValue #####
print("E's _FillValue are:")
FillValue_E=fn_nc.variables['E']._FillValue
print(FillValue_E)

##### standard_name #####
print("E's standard_name are:")
standard_name_E=fn_nc.variables['E'].standard_name
print(standard_name_E)

############# get E variable ###############
E=fn_nc.variables['E'] 
print(E.shape)

############# mask fillvalues ###############
E=np.ma.masked_values(E,FillValue_E)

############# calculate 1981 evapration all days ###############
E_year=np.transpose(np.sum(E,axis=0))
print(E_year.shape)

############# get lat variable and lat_min, lat_max ###############
lat=fn_nc.variables['lat']
lat_min=np.min(lat)
lat_max=np.max(lat)

############# get lon variable and lon_min, lon_max ###############a
lon=fn_nc.variables['lon']
lon_min=np.min(lon)
lon_max=np.max(lon)

############# plot ###############
plt.figure(figsize=(40,30))
plt.subplot(1,1,1)

############# set projection ###############

##### geographic projection #####
m=Basemap(projection='cyl',llcrnrlon=lon_min,urcrnrlon=lon_max,llcrnrlat=lat_min,urcrnrlat=lat_max,resolution='l')

##### Robinson projection #####
m=Basemap(projection='robin',lon_0=0,lat_0=0,resolution='l')

##### generate lon and lat grid #####
lon,lat=np.meshgrid(lon,lat)

##### exchange the lon and lat into the projection lon and lat #####
lon,lat=m(lon,lat)

##### plot the continent lines #####
m.drawcoastlines(linewidth=0.2)

##### plot the lon and lat lines #####
m.drawparallels(np.arange(-90, 90,30), labels=[1,0,0,0], fontsize=13,linewidth=0.8)
m.drawmeridians(np.arange(-180, 180, 45), labels=[0,0,0,1], fontsize=13,linewidth=0.8)

##### set colorbar #####
cmap = plt.cm.jet_r
norm = matplotlib.colors.Normalize(vmin=-50, vmax=2100)

##### plot the data #####
##### contour plot #####
#cf=plt.contourf(lon,lat,E_year,20,cmap=cmap,norm=norm)

##### show values #####
#cf=m.imshow(E_year[::-1],cmap=cmap,norm=norm)

##### mesh #####
cf=plt.pcolormesh(lon,lat,E_year,cmap=cmap,norm=norm)

##### set the title #####
plt.title("Global Actual Evaporation in 1980",fontsize=18) 

##### plot the colorbar #####
##### colorbar location x,y and width,height #####
cax=plt.axes([0.9, 0.11, 0.018,0.77])
cbar=plt.colorbar(cf,cax=cax)

##### colorbar ticklabels #####
cbar.ax.tick_params(labelsize=13, direction='in')

##### colorbar label ######
font = {'family' : 'Times New Roman',   
        'weight' : 'normal',  
        'size'   : 15,  
        } 
cbar.set_label(r'Evaporation (mm)',fontdict=font)

##### save the figure #####
plt.savefig(r'C:\Users\shaoqi_i\Desktop\evaporation.tif',dpi=100)

##### show the plot #####
plt.show()
