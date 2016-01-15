# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 00:02:00 2015

@author: Cai Jiawen
"""

import seaborn as sns

z = [[0,2,4,6,8],
     [1,0,2,4,6],
     [2,1,0,2,4],
     [3,2,1,0,2],
     [4,3,2,1,0]]
     
sns.heatmap(z, annot=True, linewidths=.5,xticklabels=False,yticklabels=False)