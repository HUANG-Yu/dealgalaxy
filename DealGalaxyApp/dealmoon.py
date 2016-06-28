#!/usr/bin/env python

import sys
import json
import datetime
import random
import datetime
import string
import pprint
import psycopg2
from pandas import read_sql
from datetime import date, timedelta
from flask import Flask, render_template, redirect, request

app = Flask(__name__)

def get_time():
    time  = datetime.datetime.now()
    # round to the next full hour
    time -= datetime.timedelta(minutes = time.minute, seconds = time.second, microseconds =  time.microsecond)
    time += datetime.timedelta(hours = 1)
    time_string = time.strftime("%Y-%m-%d_%H-%M")
    # print time_string
    return time_string

@app.route('/') 
def defaultindex():
    return render_template('index.html')

@app.route('/index') 
def index():
    return render_template('index.html')

@app.route('/cheapestfinder/') 
def cheapestfinder():
    return render_template('blank-page.html')

@app.route('/cheapestsearch/<itemname>') 
def cheapestsearch(itemname):
    conn = psycopg2.connect(conn_string)
    # print itemname
    df = read_sql("select price, couponcode, websitename from discountprice where crawldate=\'2016-06-21\' and itemname=\'" + str(itemname) + "\' order by price limit 5", con=conn)
    conn.commit()
    conn.close()
    data = df.to_json(orient='records')
    # print data
    return render_template('blank-page.html', cheapest=data, jsondata = '[]')

@app.route('/itemsearch/<itemname>') 
def itemsearch(itemname):
    conn = psycopg2.connect(conn_string)
    df = read_sql("select distinct itemname from item where crawldate=\'2016-06-20\' and itemname LIKE \'%" + str(itemname) + "%\' limit 15", con=conn)

    conn.commit()
    conn.close()
    data = df.to_json(orient='records')
    if data:
        # print data
        return render_template('blank-page.html', jsondata = data, cheapest = '[]', itemname=itemname)
    else:
        return render_template('blank-page.html', itemname=itemname)

@app.route('/hotdeals/')
def hotdeals():
    today = get_time()
    conn = psycopg2.connect(conn_string)
    df = read_sql("select a.websitename, a.couponcode, b.category, a.discount from website as a, coupon as b where a.crawldate=\'2016-06-20\' and a.couponcode=b.couponcode order by a.discount desc limit 100", con=conn)
    conn.commit()
    conn.close()
    # print df.to_json(orient='records')
    return render_template('hotdeals-result.html', websites=df.to_json(orient='records'))

@app.route('/websitesearch/<websitename>')
def websitesearch(websitename):
    conn = psycopg2.connect(conn_string)
    df = read_sql("select crawldate, cashback from ebates where websitename=\'" + str(websitename) + "\' order by crawldate", con=conn)
    conn.commit()
    conn.close()
    if df.to_json(orient='records'):
        data = df.to_json(orient='records')
        # print data
        return render_template('ebates.html', jsondata = data, websitename=websitename)
    else:
        return render_template('ebates.html', websitename=websitename)

@app.route('/todo/')
def todo(name=None):
    return render_template('bootstrap-elements.html')

@app.route('/element/')
def element(name=None):
    return render_template('bootstrap-elements.html')

@app.route('/ebay/')
def ebay():
    conn = psycopg2.connect(conn_string)
    df1 = read_sql("select count(*) from ebay where buyitnow=\'false\'", con=conn)
    df2 = read_sql("select count(*) from ebay where buyitnow=\'true\'", con=conn)
    conn.commit()
    conn.close()
    # print df1
    return render_template('ebay.html', falsecount = df1.to_json(orient='records'), truecount = df2.to_json(orient='records'))

@app.route('/ebates/')
def ebates(name=None):
    return render_template('ebates.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug = True)