# coding=utf-8

import urllib2
import random,json
import tushare as ts
import histprovider

from itertools import groupby
from operator import itemgetter


class ApplicationCache:
    stock_basic=None
    hasCacheStockInfo=False
    stockDict={}


def getResult(codeArr):
    result=[]
    for item in codeArr:
        result.append(fetchFromTushare(item))

    result=sorted(result,key=itemgetter(1),reverse=True)
    return  result


def fetchFromTushare(code):
    print(code)
    if ApplicationCache.hasCacheStockInfo==False:
        print('no cash')
        ret=ts.get_stock_basics()
        ApplicationCache.stock_basic=ret
        ApplicationCache.hasCacheStockInfo=True
        for row in ret.iterrows():
            if not ApplicationCache.stockDict.has_key(row[0]):
                ApplicationCache.stockDict[row[0]]=row[1]['name']
    for row in ApplicationCache.stock_basic.iterrows():
        if row[0]==code:
            if row[1]['pe'] == 0:
                return [row[0]+' '+row[1]['name'],0]
            else:
                return [row[0]+' '+row[1]['name'],float(row[1]['pb'])/float(row[1]['pe'])]

    return []


def _getHistOnline(codes,startDate,endDate):
    datesArr=[]
    series=[]

    for code in codes:
        haskey=ApplicationCache.stockDict.has_key(code)
        name=  ApplicationCache.stockDict[code] if haskey else code
        item={'name':name+' '+code,'data':[]}

        ret=ts.get_hist_data(str(code),start=startDate,end=endDate)
        for row in ret.iterrows():
            if row[0] not in datesArr:
                    datesArr.append(row[0])
            item['data'].append(row[1]['close'])

        series.append(item)
    return (datesArr,series)


def _getHistFromDB(codes,startDate,endDate):
    datesArr=[]
    series=[]

    rows=histprovider.select(codes,startDate,endDate)

    rows=sorted(rows,key=itemgetter(0))
    for code,lst in groupby(rows,lambda k : k[0]):
        haskey=ApplicationCache.stockDict.has_key(code)
        name=  ApplicationCache.stockDict[code] if haskey else code
        item={'name':name+' '+code,'data':[]}
        for row in lst:
            item['data'].append(row[1])
        series.append(item)

    rowofDate=sorted(rows,key=itemgetter(2))
    for date,lst in groupby(rowofDate,lambda  k: k[2]):
        if date not in datesArr:
                    datesArr.append(date)

    return (datesArr,series)


def getHist(codes,startDate,endDate):
    return _getHistFromDB(codes,startDate,endDate)


if __name__ == '__main__':
    ret=getResult(['002230','002736','600030'])
    print(ret)

