# coding=utf-8

import urllib2
import random,json
import tushare as ts


class ApplicationCache:
    stock_basic=None
    hasCacheStockInfo=False
    stockDict={}


def getResult(codeArr):
    result=[]
    for item in codeArr:
        result.append(fetchFromTushare(item))
    return  result


def fetchFromTushare(code):
    if ApplicationCache.hasCacheStockInfo==False:
        ret=ts.get_stock_basics()
        ApplicationCache.stock_basic=ret
        for row in ret.iterrows():
            if not ApplicationCache.stockDict.has_key(row[0]):
                ApplicationCache.stockDict[row[0]]=row[1]['name']
    for row in ApplicationCache.stock_basic.iterrows():
        if row[0]==code:
            return [row[0]+' '+row[1]['name'],row[1]['pe'],row[1]['pb']]
    return []

def fetch(code):
    #rsp='v_sz002230="51~科大讯飞~002230~55.85~55.52~55.54~510890~255196~255694~55.85~24~55.84~567~55.83~12~55.82~6~55.81~8~55.86~121~55.87~871~55.88~470~55.89~333~55.90~1023~15:00:22/55.85/5249/S/29312872/17973|14:57:00/55.87/87/B/485897/17827|14:56:57/55.85/178/M/994477/17824|14:56:54/55.87/154/M/860320/17821|14:56:49/55.88/136/B/762704/17816|14:56:48/55.88/175/B/977722/17813~20150522150504~0.33~0.59~56.50~53.50~55.87/505641/2766388450~510890~279570~5.73~171.28~~56.50~53.50~5.40~497.58~676.78~11.68~61.07~49.97~'
    url='http://qt.gtimg.cn/q='+code
    try:
        rsp=urllib2.urlopen(url).read()
        print(rsp)
        return parserResult(rsp)
    except:
        print('urlopen:'+url+' failed!')
        return []

def fetchFromXueqiu(code):
    try:
        code=code.upper()
        url='http://xueqiu.com/v4/stock/quote.json?code={0}&_=1432475267{1}'.format(code,random.randint(100,1000))

        #rsp=urllib2.urlopen(url).read()
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'fake-client')
        request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8');
        #request.add_header('Accept-Encoding','gzip, deflate, sdch');
        request.add_header('Accept-Language','zh-CN,zh;q=0.8');
        request.add_header('Cache-Control','max-age=0');
        request.add_header('Connection','keep-alive');
        request.add_header('Cookie','s=ia3xe6kp.4dqj1rg; xq_a_token=d15761b2bcfdadef2c59e38b9e8f3df119aa8bf9; xq_r_token=81c1baca9449cbb0cb8087503c6fe41027d95b58; __utma=1.1733120944.1432560268.1432560268.1432560268.1; __utmb=1.1.10.1432560268; __utmc=1; __utmz=1.1432560268.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_1db88642e346389874251b5a1eded6e3=1432388642,1432475101; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1432560268');
        request.add_header('Host','xueqiu.com');
        request.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 Safari/537.36');
        rsp = urllib2.urlopen(request).read()
        print(rsp)
        obj=json.loads(rsp)[code]
        return [obj['name']+' '+obj['code'],obj['pe_lyr'],obj['pb']]
    except:
        print('fetchFromXueqiu failed:'+url)
        return []

def parserResult(str):
    if len(str)<1:
        return []

    arr=str.split('~')
    if len(arr)<35:
        return  []

    company=arr[1].decode('gbk').encode('utf-8')
    return [company+' '+arr[2],arr[39],arr[46]]


def getHist(codes,startDate,endDate):
    datesArr=[]
    series=[]
    for code in codes:
        item={'name':code,'data':[]}
        ret=ts.get_hist_data(str(code),start=startDate,end=endDate)
        for row in ret.iterrows():
            if row[0] not in datesArr:
                if ApplicationCache.stockDict.has_key(row[0]):
                    datesArr.append(ApplicationCache.stockDict[row[0]+' '+row[0]])
                else:
                    datesArr.append(row[0])
            item['data'].append(row[1]['close'])
        series.append(item)
    return (datesArr,series)


if __name__ == '__main__':
    ret=getResult(['002230','002736'])
    print(ret)

