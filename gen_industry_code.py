# coding=utf-8
__author__ = 'haozes'


import  urllib2,json
url_page1='http://q.10jqka.com.cn/interface/stock/thshy/zdf/desc/{0}/quote/quote'

url_stocks='http://q.10jqka.com.cn/interface/stock/detail/zdf/desc/{page}/1/{plate}'



def _requestJSON(url):
    rsp=urllib2.urlopen(url).read()
    return json.loads(rsp)

def _getPlate(obj):
    return [obj['platename'],obj['hycode']]

def _getPlates():
    plates=[]
    for i in range(1,3):
        obj=_requestJSON(url_page1.format(i))
        for item in obj['data']:
            plates.append(_getPlate(item))
    return plates

def getPlateStockCode(hycode):
    arr=[]
    num=1
    flag=True
    while (flag):
        obj=_requestJSON(url_stocks.format(page=num,plate=hycode))
        for item in obj['data']:
            arr.append(item['stockcode'])
        if len(obj['data'])>49:
            num=num+1
        else:
            flag=False
    return arr


def getData():
    plateStockDict={};
    for p in _getPlates():
        plateName=p[0];
        hycode=p[1];
        plateStockDict[plateName]=getPlateStockCode(hycode)
    print(plateStockDict)
    return plateStockDict


output = open('plate_stock.json', 'wb')
json.dump(getData(),output)

