# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 00:46:13 2015

@author: Cai Jiawen
"""
import mechanize
import requests
from bs4 import BeautifulSoup

url = "http://jingzhi.funds.hexun.com/fb/zhejia.aspx"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'}
payload = {'enddate':'2015-12-25'}


res = requests.post("http://jingzhi.funds.hexun.com/fb/zhejia.aspx",headers=headers,data=payload)
Soup = BeautifulSoup(res.text)
DateSoup = soup.find('select', attrs = {'name':'enddate'})





br = mechanize.Browser()
br.open(res)