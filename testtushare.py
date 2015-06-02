# coding=utf-8


import tushare as ts
import json

def getHist(codes,startDate,endDate):
    datesArr=[]
    series=[]
    for code in codes:
        item={'name':code,'data':[]}
        ret=ts.get_hist_data(str(code),start=startDate,end=endDate)
        for row in ret.iterrows():
            if row[0] not in datesArr:
                datesArr.append(row[0])
            item['data'].append(row[1]['close'])
        series.append(item)
    return (datesArr,series)

#ret=getHist(['002230'],'2015-05-20','2015-05-26')
#ret=ts.get_hist_data('002230','2015-05-24','2015-05-31')


ret=ts.get_concept_classified()

for row in ret.iterrows():
    print(row[0],row[1]['code'],row[1]['name'],row[1]['c_name'])