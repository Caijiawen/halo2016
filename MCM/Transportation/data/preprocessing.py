# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 09:34:43 2016

@author: Cai Jiawen
"""

import codecs
import re
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from ggplot import *
#import datetime
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8') 

#df = pd.read_csv("accident.csv",index='\xef\xbb\xbfaccidenttime',parse_dates=True)
#df.columns = [var.strip() for var in df.columns]
#df['\xef\xbb\xbfaccidenttime']
#df.iloc[:5,:]

#f = codecs.open('accident.csv','r','utf-8')
#for line in f:
#    print line.strip().split(",")
#    break
df = pd.read_csv("accident.csv",encoding="utf-8")

def parse_date(date_str):
    t = date_str.split(' ')
    year = int(t[0].split('-')[0])    
    month = int(t[0].split('-')[1])
    day = int(t[0].split('-')[2])
    hour = float(t[1].split(':')[0])+float(t[1].split(':')[1])/60
    return year,month,day,hour
    
def color_replace(color):
    parsed_color = color.replace(u'色',"")
    if parsed_color not in [u'白',u'银',u'蓝',u'棕',u'灰',u'红',u'绿',u'黄',u'黑']:
        if parsed_color in [u'拔丝',u'表示',u'BAI',u'北']:
            parsed_color = u'白'
        elif parsed_color==u'Y银':
            parsed_color = u'银'
        elif parsed_color==u'兰':
            parsed_color = u'蓝'
        else:
            parsed_color = u"-1"
    return parsed_color            


def birth_parse(birth):
    try:
        birth_year = int(birth[:4])
        age = 2016-birth_year
        month = int(birth[4:])    
    except:
        age = 30
        month = int(np.random.choice(12,1)+1)
    if age<0 or age>100:
        age = 30
        month = int(np.random.choice(12,1)+1)
    return age,month
    
def drive_time(time):
    try:
        t = time.split(' ')
        year = int(t[0].split('-')[0])    
        month = int(t[0].split('-')[1])
        return (2016-year)-float(month)/12
    except:
        return -1


#%%事故时间
df['acc_year'],df['acc_month'],df['acc_day'],df['acc_hour'] =  zip(*df[df.columns[0]].map(parse_date))


#%%事故地点
df['accidentaddr'] = df['accidentaddr'].map(lambda x: u"贵阳"+x)
#df['accidentaddr'].value_counts()

#%%事故类型
df['acc_type'] = df['driver1fault'].map(lambda x:x.split(u"、")[0])

#%%事故责任


#%%车辆颜色
df['carcolor1'] = df['carcolor1'].str.strip()  
df['carcolor1'] = df['carcolor1'].apply(color_replace) 
df['carcolor2'] = df['carcolor2'].str.strip()  
df['carcolor2'] = df['carcolor2'].apply(color_replace)  

#carcolor1 = df['carcolor1'].astype("category")
#print carcolor1.cat.categories
#print carcolor1.value_counts()
#carcolor1.value_counts().plot(kind='bar')


#%%出生日期,月份
#df['brith1'].apply(birth_parse)

df['age'],df['birthmonth'] = zip(*df["brith1"].map(birth_parse))
#df['age'].value_counts()


#%%驾龄

df['drive_time1'] = df["cclzrq1"].map(drive_time)
df['drive_time2'] = df["cclzrq2"].map(drive_time)


#%%输出用作描述frame
descriptive_columns =[]
acc_columns=['driver1responsibility','acc_type','acc_month','acc_hour','accidentaddr']
driver_columns = ['age','birthmonth','sex1','drive_time1','jxmc1']
car_columns = ['carcolor1','clpp1']
descriptive_columns.extend(acc_columns)
descriptive_columns.extend(driver_columns)
descriptive_columns.extend(car_columns)

descriptive_frame = pd.DataFrame()
for i in descriptive_columns:
    descriptive_frame[i] = df[i]


#%%Spatial Visualization
fullRes = descriptive_frame[descriptive_frame['driver1responsibility']==u'负全部责任']
fullRes['accidentaddr'].value_counts()

#在贵阳地图上画柱子或者点点
#1.通过高德或百度获取经纬度
#2.通过echart或其他可视化工具绘画
from bokeh.io import output_file, show
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool
)

geo_visual = pd.read_csv("guiyangmap.csv",encoding="utf-8")

gy_lon = geo_visual['lon']
gy_lat = geo_visual['lat']
gy_count = geo_visual['count']
gy_count_size = gy_count/15

map_options = GMapOptions(lat=gy_lat.mean(), lng=gy_lon.mean(), map_type="roadmap", zoom=11)

plot = GMapPlot(
    x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, title="Guiyan Car Accident"
)

source = ColumnDataSource(
    data=dict(
        lat=list(gy_lat),
        lon=list(gy_lon),
        count = list(gy_count_size)
    )
)

circle = Circle(x="lon", y="lat", size="count", fill_color="blue", fill_alpha=0.8, line_color=None)
plot.add_glyph(source, circle)

plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
output_file("gmap_plot.html")
show(plot)


#%%Variable Visualization


#事故种类柱状图
ggplot(aes(x='acc_type'), data=fullRes) + \
     geom_bar()

#哪个时段事故多？
ggplot(aes(x='acc_hour'), data=fullRes) + \
     geom_density()

ggplot(aes(x='acc_hour'), data=fullRes) + \
     geom_density()+facet_grid('acc_type')

#什么年龄的人喜欢犯错误？

ggplot(aes(x='age'), data=fullRes) + \
     geom_density()


#那个月份出生的人喜欢追尾？（星座喜欢什么颜色的车？）

ggplot(aes(x='birthmonth',fill='acc_type', color='acc_type'), data=fullRes) + \
     geom_histogram(binwidth=1,alpha=0.6)+xlim(1,12)


#女司机危险还是男司机危险？（男女司机数量本来不同，得到男女司机总量再做评价）


#什么驾校培养追尾大王
ggplot(aes(x='acc_type'), data=fullRes) + \
     geom_bar()



#老司机是不是不乱飙车？
ggplot(aes(x='drive_time1'), data=fullRes) + \
     geom_density()+xlim(0,35)



#%%处理分类变量,encoder


#for f in df.columns:#
#    if df[f].dtype=='object':
#        lbl = LabelEncoder()
#        lbl.fit(list(df[f]))
#        df[f] = lbl.transform(list(df[f].values))
#        


#%%缺失值
#df.fillna(u"-1")


#%%输出用作模型csv
#result = pd.DataFrame()


