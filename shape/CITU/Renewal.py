#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
sys.path.append('/data/www/stock/')
import tushare as ts
import numpy as np
import pandas as pd
import time
import re
from config.db_config import stock_db
from data.Date import Date
from data.Stock import Stock

reload(sys)
sys.setdefaultencoding('utf-8')

class Renewal:

    def __init__(self, secCode, secName, secID):
        self.secCode = secCode
        self.secName = secName
        self.secID = secID
        #self._date = time.strftime('%Y%m%d', time.localtime(time.time()))
        self._date = '20181031'

    """
    获取形态运行中的股票
    """
    def getOperationStock(self):
        sql = """SELECT * FROM shape WHERE stage = %d AND appear_date != '%s' AND deleted_at IS NULL""" % (200, Date.getDateAmend(self._date))
        return stock_db.fetch_all(sql)

    """
    更新收益
    """
    def handel(self):
        data = self.getOperationStock()
        print data
        for i in range(0, len(data)):
            cal = Stock.getStockCal(data[i]['sec_code'], Date.getDateAmend(self._date), Date.getDateAmend(self._date))
            print cal
            if len(cal) <= 0:
                continue
            morrowIncome = data[i]['morrow_income']
            morrowPrice = data[i]['morrow_price']
            winRate = data[i]['win_rate']
            castDate = data[i]['cast_date']
            income = (cal[0]['close'] - data[i]['join_price']) / data[i]['join_price']
            if data[i]['total_position'] == 0:
                morrowIncome = income
                morrowPrice = cal[0]['close']

            highIncome = data[i]['high_income']
            highPrice = data[i]['high_price']
            highPosition = data[i]['high_position']
            if highIncome < income:
                highIncome = income
                highPrice = cal[0]['close']
                highPosition = data[i]['total_position']+1
                castDate = Date.getDateAmend(self._date)

            periods = data[i]['total_position']+1
            totalIncome = income
            totalPrice = cal[0]['close']
            if data[i]['total_position'] == 9:
                stage = 300
            upSql = """UPDATE shape SET cast_date = '%s' AND morrow_income = '%f' AND morrow_price = '%f' AND high_income = '%f' AND high_price = '%f' AND total_income = '%f' \
 AND total_price = '%f' AND best_position = '%d' AND total_position = '%d' AND win_rate = '%f' AND stage = '%d' AND updated_at = '%d' WHERE id = '%d'""" % (castDate, \
morrowIncome, morrowPrice, highIncome, highPrice, totalIncome, totalPrice, highPosition, periods, winRate, stage, int(time.time()), data[i]['id'])
            stock_db.update(upSql)
        return True

class Stock:
    def getStockAll(self):
        with open('/data/share/loudou/stock/stockTicker.txt', 'r') as f:
            lines = [line.strip() for line in f.readlines()]
        return lines

#
# stock = Stock()
#sk = stock.getStockAll()
sk = ["601518-吉林高速-601518.SH"]
for tk in sk:
    try:
        sec = re.split("-", tk)
        renewal = Renewal(sec[0], sec[1], sec[2])
        res = renewal.getOperationStock()
        print sec[2]
    except Exception, data:
        print data