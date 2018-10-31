#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
sys.path.append('/data/www/stock/')
import tushare as ts
import numpy as np
import pandas as pd
import redis
import time
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

        succee = 0
        defeated = 0
        for i in range(dataLen-1, -1, -1):
            print data[i]['date']
            if data[i]['close'] > data[i]['open']:
                continue
            if data[i]['low'] < data[i-1]['open']:
                continue
            if data[i]['open'] < data[i-1]['close']:
                continue
            average = (data[i]['open']+data[i]['close'])/2
            if data[i-1]['close'] < average:
                continue
            if data[i-1]['close'] < data[i-2]['close']:
                is_succee = 20
                succee = succee+1
            else:
                defeated = defeated+1
                is_succee = 10

            morrowIncome = (data[i-2]['close']-data[i-1]['close'])/data[i-1]['close']
            morrowPrice = data[i-2]['close']
            appearDate = data[i-1]['date']
            castDate = data[i-1]['date']
            highIncome = 0
            highPrice = 0
            highPosition = 0
            winRate = 0
            totalPositio = period
            totalIncome = 0
            totalPrice = 0

            stage = 300
            if (i-period)<0:
                stage = 200

            if i!=0:
                for j in range(2, period + 2):
                    income = (data[i - j]['high'] - data[i - 1]['close']) / data[i - 1]['close']
                    if income > highIncome:
                        castDate = data[i - j]['date']
                        highIncome = income
                        highPrice = data[i - j]['high']
                        highPosition = j - 1

                totalIncome = (data[i - (period + 1)]['close'] - data[i - 1]['close']) / data[i - 1]['close']
                totalPrice = data[i - (period + 1)]['close']
                winRate = succee / float((succee + defeated))

            sql = """INSERT INTO shape (shape_key, sec_code, sec_name, is_succee, appear_date, cast_date, morrow_income, morrow_price, high_income, \
high_price, total_income, total_price, best_position, total_position, win_rate, stage, created_at, updated_at) VALUES ('%s', \
'%s', '%s', '%d', '%s', '%s', '%f', '%f', '%f', '%f', '%f', '%f', '%d', '%d', '%f', '%d',  '%d', '%d')""" % ('CITU', self.secCode, self.secName, \
is_succee, appearDate, castDate, morrowIncome, morrowPrice, highIncome, highPrice, totalIncome, totalPrice, highPosition, totalPositio, winRate, stage, int(time.time()), int(time.time()))
            id = stock_db.insertData(sql)
            if id > 0:
                for k in range(0, 2):
                    shapeDetail = """INSERT INTO shape_detail (shape_id, shape_date, shape_price, shape_income, created_at, updated_at) VALUES ('%d', '%s','%f', '%f', '%d', '%d')""" % ( \
                        id, data[i+k]['date'], data[i+k]['price'], data[i+k]['p_change'], int(time.time()),
                        int(time.time()))
                    stock_db.insertData(shapeDetail)
        return True

class Stock:
    def getStockAll(self):
        with open('/data/share/loudou/stock/stockTicker.txt', 'r') as f:
            lines = [line.strip() for line in f.readlines()]
        return lines

#stock = Stock()
#sk = stock.getStockAll()
sk = ["601518-吉林高速"]
for tk in sk:
    try:
        sec = tk.partition("-")
        history = History(sec[0], sec[2])
        res = history.handel('2016-01-01', '2018-11-01', 10)
        print sec[2]
    except:
        continue