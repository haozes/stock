__author__ = 'jhwang'

import sqlite3
from datetime import *

import time,functools
import tushare as ts

DATABASE = '../stock.db'


def time_me(info="used"):
  def _time_me(fn):
    @functools.wraps(fn)
    def _wrapper(*args, **kwargs):
      start = time.clock()
      fn(*args, **kwargs)
      print("{0} {1} {2}".format(fn.__name__, info, time.clock() - start), "second")
    return _wrapper
  return _time_me

def saveOrUpdate(code,price,date):
    execute('insert into history(code,price,date) values (?,?,?)',[code,price,date])

def select(codes,startDate,endDate):
    sql='select * from history where code in ({0})'.format(', '.join('\''+c+'\'' for c in codes))
    sql=sql+' and date>? and date<?'
    print(sql)
    return query_db(sql,[startDate,endDate])

def get_db():
    db = sqlite3.connect(DATABASE)
    return db

def execute(query,args=()):
    conn=get_db()
    cur=conn.cursor()
    cur.execute(query,args)
    conn.commit()


def setPRAGMA(RRAGMA="ON"):
    conn=get_db()
    cur=conn.cursor()
    if RRAGMA=="OFF":
        cur.execute("PRAGMA synchronous = OFF")
    else:
        cur.execute("PRAGMA synchronous = ON")

def query_db(query, args=(), one=False):
    cur=get_db().cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@time_me()
def insertHistory():
    today=datetime.today()
    n=10
    conn=get_db()
    cur=conn.cursor()
    cur.execute("PRAGMA synchronous = OFF")

    info=ts.get_stock_basics()
    for item in info.iterrows()
        code=item[0]
        hist=ts.get_hist_data(code,'2014-01-01','2015-05-31')
        for row in hist.iterrows():

            date=row[0]
            price=row[1]['close']
            cur.execute('insert into history(code,price,date) values (?,?,?)',[code,price,date])
            conn.commit()

            print(code,date,price)


insertHistory()
