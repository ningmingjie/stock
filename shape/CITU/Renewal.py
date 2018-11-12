#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
sys.path.append('/data/www/stock/')
import tushare as ts
import numpy as np
import pandas as pd
import time
import re
import math
from config.db_config import stock_db
from data.Date import Date
from data.Stock import Stock as StockUD

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

        for i in range(0, len(data)):
            cal = StockUD.getStockCal(data[i]['sec_code'], Date.getDateAmend(self._date), Date.getDateAmend(self._date))
            if len(cal) <= 0:
                continue

            morrowIncome = data[i]['morrow_income']
            morrowPrice = data[i]['morrow_price']
            winRate = data[i]['win_rate']
            castDate = data[i]['cast_date']
            income = (cal[0]['close'] - data[i]['join_price']) / data[i]['join_price']
            is_succee = data[i]['is_succee']
            if data[i]['total_position'] == 1:
                count = """SELECT COUNT(*) as ct FROM shape WHERE sec_code = %s AND deleted_at IS NULL""" % (data[i]['sec_code'])
                count = stock_db.fetch_one(count)
                if cal[0]['close'] > data[i]['join_price']:
                    is_succee = 20
                    winRate = math.ceil(winRate*count['ct'])+1 / float(count['ct'])
                else:
                    is_succee = 10
                    rtCount = math.ceil(winRate * count['ct'])
                    rtCount = 0 if(rtCount-1<0) else rtCount-1
                    winRate = rtCount / float(count['ct'])

                morrowIncome = income
                morrowPrice = cal[0]['close']

            highIncome = data[i]['high_income']
            highPrice = data[i]['high_price']
            highPosition = data[i]['best_position']
            if highIncome < income:
                highIncome = income
                highPrice = cal[0]['close']
                highPosition = data[i]['total_position']+1
                castDate = Date.getDateAmend(self._date)

            periods = data[i]['total_position']+1
            totalIncome = income
            totalPrice = cal[0]['close']
            stage = 200
            if data[i]['total_position'] == 9:
                stage = 300
            upSql = """UPDATE shape SET is_succee = '%d', cast_date = '%s', morrow_income = '%f', morrow_price = '%f', high_income = '%f', high_price = '%f', total_income = '%f' \
, total_price = '%f', best_position = '%d', total_position = '%d', win_rate = '%f', stage = '%d', updated_at = '%d' WHERE id = '%d'""" % (is_succee, castDate, \
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
        res = renewal.handel()
        print sec[2]
    except Exception, data:
        print data