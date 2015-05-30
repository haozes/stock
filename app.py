# coding=utf-8

from flask import Flask,send_from_directory,request,jsonify
from flask import render_template
import json
import parser
import sys

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__,static_url_path='')

@app.route('/')
def main():

    return render_template('main.html')

@app.route('/get',methods=['POST'])
def get():
    stocks=request.json['arr']

    arr=[]
    for item in stocks:
        str=item.decode('gbk').encode('utf-8')
        arr.append(str)

#        if str.startswith('6'):
#            arr.append('sh'+str)
#        else:
#            arr.append('sz'+str)

    ret=parser.getResult(arr)
    return jsonify(results=ret)


@app.route('/gethist',methods=['POST'])
def history():
    stocks=request.json['codes']
    start=request.json['start']
    end=request.json['end']
    ret=parser.getHist(stocks,start,end)
    return jsonify(results=ret)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)


@app.route('/hello')
def hello():
    return 'Hello World'

if __name__ == '__main__':
    app.debug=True
    app.run(port=1986)