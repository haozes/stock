# coding=utf-8
__author__ = 'haozes'


import json

import tushare as ts


ret=ts.get_stock_basics()

hst={}
for row in ret.iterrows():
    if row[1]['pe'] == 0:
        hst[row[0]] = (row[1]['name'],0)
    else:
        hst[row[0]]=(row[1]['name'],float(row[1]['pb'])/float(row[1]['pe'])*100)


output = open('ratio.json', 'wb')

json.dump(hst,output)
