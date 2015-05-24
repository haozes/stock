# coding=utf-8

import urllib2

def getResult(codeArr):
    result=[]
    for item in codeArr:
        result.append(fetch(item))
    return  result


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


def parserResult(str):
    if len(str)<1:
        return []

    arr=str.split('~')
    if len(arr)<35:
        return  []

    company=arr[1].decode('gbk').encode('utf-8')
    return [company+' '+arr[2],arr[39],arr[46]]

'''

if __name__ == '__main__':
    ret=getResult(['sz002230','sz002690'])
    print(ret)

'''