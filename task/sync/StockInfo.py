#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
sys.path.append('/data/www/stock/')
import tushare as ts
import time
from config.db_config import stock_db
from data.Date import Date

reload(sys)
sys.setdefaultencoding('utf-8')

class StockInfo:
    def __init__(self):
        ts.set_token('9caf3d505f4f4b5cefd16f25c533e1cae081773442c216888678ddee')
        self._endDate = time.strftime('%Y%m%d',time.localtime(time.time()))

    #查询当前所有正常上市交易的股票列表
    def getQuery(self):
        pro = ts.pro_api()
        data = pro.query('stock_basic', exchange_id='', list_status='L', fields= \
'ts_code, symbol, name, area, industry, fullname, enname, market, exchange_id, curr_type, list_status, list_date, delist_date, is_hs')
        #print data
        return data.to_dict('records')

    #写入数据
    def insertStockInfo(self):
        data = self.getQuery()
        for i in range(0, len(data)):
            delistDate = '1970-01-01'
            if data[i]['delist_date'] != None:
                delistDate = Date.getDateAmend(data[i]['delist_date'])
            sql = """INSERT INTO stock_info (sec_id, sec_code, sec_name, area, industry, fullname, market, exchange_id, curr_type, list_status, list_date,\
 delist_date, is_hs, created_at, updated_at) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%d')""" % (data[i]['ts_code'], \
data[i]['symbol'], data[i]['name'], data[i]['area'], data[i]['industry'], data[i]['fullname'], data[i]['market'], data[i]['exchange_id'], data[i]['curr_type'], \
data[i]['list_status'], Date.getDateAmend(data[i]['list_date']), delistDate, data[i]['is_hs'], int(time.time()), int(time.time()))
            stock_db.insertData(sql)

        return True

stock = StockInfo()
stock.insertStockInfo()