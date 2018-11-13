#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
sys.path.append('/data/www/stock/')
import tushare as ts
import numpy as np
import pandas as pd
import time
import re
from data.Date import Date
from data.Stock import Stock as StockUD
from config.db_config import stock_db

reload(sys)
sys.setdefaultencoding('utf-8')

class Present:

    def __init__(self, secCode, secName, secID):
        self.secCode = secCode
        self.secName = secName
        self.secID = secID
        self._date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        #self._date = '2018-10-30'
        self._lastCalDate = StockUD.getLastSecCalDate(secCode, self._date)

    """
    获取近两日行情数据
    startDay ：开始时间
    endDay ：结束时间
    """
    def getHistData(self):
        #获取上个交易日期
        data = ts.get_hist_data(self.secCode, self._lastCalDate, self._date)
        data.reset_index(inplace=True)
        #索引重新命名
        data.rename(
            columns={'date': 'date', 'open': 'open', 'high': 'high', 'close': 'close', 'low': 'low', 'volume': 'volume',
                     'price_change': 'price_change', 'p_change': 'p_change', 'ma5': 'ma5', 'ma10': 'ma10',
                     'ma20': 'ma20', 'v_ma5': 'v_ma5', 'v_ma10': 'v_ma10', 'v_ma20': 'v_ma20'}, inplace=True)
        #返回字典类型
        return data.to_dict('records')

    """
    计算形态
    startDay ：开始时间
    endDay ：结束时间
    """
    def handel(self):
        if StockUD.getIsStopCalDate(self._date) == True:
            return False
        if StockUD.getIsCalDate(self._date) == False:
            return False

        data = self.getHistData()

        dataLen = len(data)
        for i in range(dataLen-1, 0, -1):
            if data[i]['close'] > data[i]['open']:
                continue
            if data[i]['low'] < data[i-1]['open']:
                continue
            if data[i]['open'] < data[i-1]['close']:
                continue
            average = (data[i]['open']+data[i]['close'])/2
            if data[i-1]['close'] < average:
                continue

            is_succee = 0
            morrowIncome = 0
            morrowPrice = 0
            castDate = '1970-01-01'
            appearDate = data[i-1]['date']
            highIncome = 0
            highPrice = 0
            highPosition = 0
            winRate = 0
            totalIncome = 0
            totalPrice = 0
            stage = 200
            query = """SELECT * FROM shape WHERE sec_code = '%s' AND appear_date = '%s' AND deleted_at IS NULL""" % (self.secCode, appearDate)
            if stock_db.fetch_one(query) != None:
                continue
            sql = """INSERT INTO shape (shape_key, sec_id, sec_code, sec_name, is_succee, appear_date, cast_date, join_price, morrow_income, morrow_price, high_income, \
high_price, total_income, total_price, best_position, total_position, win_rate, stage, created_at, updated_at) VALUES ('%s', '%s', \
'%s', '%s', '%d', '%s', '%s', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%d', '%d', '%f', '%d',  '%d', '%d')""" % ('CITU', self.secID, self.secCode, self.secName, \
is_succee, appearDate, castDate, data[i-1]['close'], morrowIncome, morrowPrice, highIncome, highPrice, totalIncome, totalPrice, highPosition, 0, winRate, stage, int(time.time()), int(time.time()))

            id = stock_db.insertData(sql)
            if id > 0:
                for k in range(0, 2):
                    shapeDetail = """INSERT INTO shape_detail (shape_id, shape_date, shape_price, shape_income, created_at, updated_at) VALUES ('%d', '%s','%f', '%f', '%d', '%d')""" % ( \
                        id, data[i-k]['date'], data[i-k]['close'], data[i-k]['p_change']/100, int(time.time()), int(time.time()))
                    stock_db.insertData(shapeDetail)
                continue
        return True

class Stock:
    def getStockAll(self):
        with open('/data/share/loudou/stock/stockTicker.txt', 'r') as f:
            lines = [line.strip() for line in f.readlines()]
        return lines

stock = Stock()
sk = stock.getStockAll()
#sk = ["300011-吉林高速-601518.SH"]
for tk in sk:
    try:
        sec = re.split("-", tk)
        present = Present(sec[0], sec[1], sec[2])
        res = present.handel()
        print sec[1]
    except Exception, data:
        print data
