#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
sys.path.append('/data/www/stock/')
import tushare as ts
import numpy as np
import pandas as pd
import time
from config.db_config import stock_db

reload(sys)
sys.setdefaultencoding('utf-8')

class Renewal:

    def __init__(self, secCode, secName):
        self.secCode = secCode
        self.secName = secName
        self._date = time.strftime('%Y%m%d', time.localtime(time.time()))

    """
    获取形态运行中的股票
    """
    def getOperationStock(self):
        sql = """SELECT * FROM shape WHERE stage = 200 AND deleted_at IS NULL"""
        return stock_db.fetch_all(sql)

    """
    更新收益
    """
    def handel(self):
        data = self.getOperationStock()
        dataLen = len(data)
        for i in range(0, dataLen):
            calList = stock_db.getHistData(self.secCode, self._date, self._date)
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

            sql = """INSERT INTO shape (shape_key, sec_code, sec_name, is_succee, appear_date, cast_date, morrow_income, morrow_price, high_income, \
high_price, total_income, total_price, best_position, total_position, win_rate, stage, created_at, updated_at) VALUES ('%s', \
'%s', '%s', '%d', '%s', '%s', '%f', '%f', '%f', '%f', '%f', '%f', '%d', '%d', '%f', '%d',  '%d', '%d')""" % ('CITU', self.secCode, self.secName, \
is_succee, appearDate, castDate, morrowIncome, morrowPrice, highIncome, highPrice, totalIncome, totalPrice, highPosition,1, winRate, stage, int(time.time()), int(time.time()))
            stock_db.insertData(sql)
            id = stock_db.getLastId()

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

#
# stock = Stock()
#sk = stock.getStockAll()
sk = ["601518-吉林高速"]
for tk in sk:
    try:
        sec = tk.partition("-")
        renewal = Renewal(sec[0], sec[2])
        res = renewal.getOperationStock()
        print sec[2]
    except:
        continue