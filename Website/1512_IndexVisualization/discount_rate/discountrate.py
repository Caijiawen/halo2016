# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 22:40:13 2015

@author: Cai Jiawen
"""

# -*- coding: utf-8 -*-  
import requests
#from bs4 import BeautifulSoup
import re
import pandas as pd
import csv
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'}
payload = {'enddate':'2015-12-09'}
res = requests.get("http://jingzhi.funds.hexun.com/fb/zhejia.aspx",data=payload,headers=headers)
#print res.text
#fund_discount_list = re.findall("<td width='80' align='right' >(.*?)</td>",res.text)
#print fund_discount_list[0]
fundname = u'瑞和小康'
#namestr = re.findall("class='rbbRed'>(.*?)</a>",res.text)
#fundindex = namestr.index(fundname)
datestr = re.findall("<option value='(.*?)'",res.text)
datelist = datestr[57:60]

#print datestr[57]=='2015-12-10'
discountlist = {}
for date in datelist:
    payload = {'enddate':date}
    try:    
        res = requests.get("http://jingzhi.funds.hexun.com/fb/zhejia.aspx",data=payload,headers = headers)
        namestr = re.findall("class='rbbRed'>(.*?)</a>",res.text)
        fundindex = namestr.index(fundname)    
        fund_discount_rate = re.findall("<td width='80' align='right' >(.*?)</td>",res.text)[fundindex]
        discountlist[date] = fund_discount_rate
    except:
        pass
d = {'date':discountlist.keys(),'discountrate':discountlist.values()}
discountframe = pd.DataFrame(data = d)
final = discountframe.sort_values(by='date')
print final
pd.DataFrame.to_csv(final,'discountrate.csv',index=False,encoding='utf-8')