# coding=utf-8


import tushare as ts

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
ret=ts.get_hist_data('002230','2015-05-20','2015-05-26')

for row in ret.iterrows():
    print(row[0],row[1]['close'])

info=ts.get_stock_basics()
for item in info.iterrows():
    code=item[0]
    hist=ts.get_hist_data(code,'2014-01-01','2015-05-31')
    for row in hist.iterrows():
        print(code,row[0],row[1]['close'])


'''
ret=ts.get_stock_basics()
#print(ret[ret.name=='科大讯飞'])
stockDict={}
for row in ret.iterrows():
    if not stockDict.has_key(row[0]):
        stockDict[row[0]]=row[1]['name']

print(stockDict['002230'])
'''
