#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
sys.path.append('/data/www/stock/')
import tushare as ts
import numpy as np
import pandas as pd
import redis
from config.db_config import stock_db

reload(sys)
sys.setdefaultencoding('utf-8')

class History:

    def __init__(self, secCode, secName):
        self.secCode = secCode
        self.secName = secName

    """
    获取历史行情数据
    startDay ：开始时间
    endDay ：结束时间
    """
    def getHistData(self, startDay = '2001-12-10', endDay = '2018-10-30'):
        data = ts.get_hist_data(self.secCode, startDay, endDay)
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
    def handel(self, startDay, endDay, period):
        data = self.getHistData(startDay, endDay)
        dataLen = len(data)
        lst = []
        succee = 0
        defeated = 0
        for i in range(dataLen-1, -1, -1):
            if data[i]['close'] > data[i]['open']:
                continue
            if data[i]['low'] < data[i-1]['open']:
                continue
            if data[i]['open'] < data[i-1]['close']:
                continue
            average = (data[i]['open']+data[i]['close'])/2
            if data[i-1]['close'] < average:
                continue
            if data[i-1]['close'] > data[i-2]['open']:
                is_succee = 20
                succee = succee+1
            else:
                defeated = defeated+1
                is_succee = 10
            lst.append([data[i][0], data[i-1][0]])

            highIncome = 0
            highPrice = 0
            highPosition = 0
            for j in range(2, period+1):
                income = (data[i-j]['hight'] - data[i-1]['close'])/data[i-1]['close']
                if income > highIncome:
                    highIncome = income
                    highPrice = data[i-j]['hight']
                    highPosition = j-1
            totalIncome = (data[period+1]['close'] - data[i-1]['close'])/data[i-1]['close']
            totalPositio = period
            totalPrice = data[period+1]['close']
            winRate = succee/(succee+defeated)
            print data[i-1]['date']
            sql = """INSERT INTO shape (shape_key, sec_code, sec_name, is_succee, high_income, \
high_price, total_income, total_price, best_position, total_position, win_rate, stage, created_at, updated_at) VALUES ('%s', \
'%s', '%s', '%d', '%f', '%f', '%f', '%f', '%d', '%d', '%f', '%d',  '%d', '%d')""" % ('CITU', self.secCode, self.secName, \
is_succee, highIncome, highPrice, totalIncome, totalPrice, highPosition, totalPositio, winRate, 300, 1540649495, 1540649495)
            stock_db.insertData(sql)


class Stock:
    def getStockAll(self):
        with open('stockTicker.txt', 'r') as f:
            lines = [line.strip() for line in f.readlines()]
        return lines

#stock = Stock()
#sk = stock.getStockAll()
sk = ['002253']
result = []
for tk in sk:
    try:
        history = History(tk, '川大智胜')
        res = history.handel('2010-10-15', '2018-10-30')
    except:
        continue
print result