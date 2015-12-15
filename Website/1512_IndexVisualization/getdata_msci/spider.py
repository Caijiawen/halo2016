# -*- coding: utf-8 -*-
"""
Created on Wed Dec 09 16:43:51 2015

@author: Cai Jiawen
"""
import re
from pandas import Series,DataFrame
import pandas as pd
import csv

with open("acwi.txt","r") as f:
    txt = f.read()
    date = re.findall('date:"(.*?)"',txt)
    msci = re.findall('value:"(.*?)"',txt)

#msci_series = Series(msci,index =date)
d = {'date':date, 'msci':msci}
msci_data = DataFrame(data=d)
print msci_data

DataFrame.to_csv(msci_data,'acwi.csv',index=False)
