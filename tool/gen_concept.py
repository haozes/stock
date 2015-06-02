# coding=utf-8


import tushare as ts
import json


def gen_data():
	ret=ts.get_concept_classified()
	arr=[]
	for row in ret.iterrows():
		arr.append((row[1]['code'],row[1]['name'],row[1]['c_name']))
	output = open('data.json', 'wb')
	json.dump(arr,output)

def gen_cxt():
    gen_data()
    cxt={}
    num=0
    with open('data.json') as data_file:
        data = json.load(data_file)
        for i,k in groupby(data,itemgetter(2)):
            num=num+1
            print(i)
            lst=[]
            for arr in tuple(k):
                lst.append((arr[0],arr[1]))
            cxt[i]=lst
        print(str(num))
        return cxt


print(json.dumps(gen_cxt()))