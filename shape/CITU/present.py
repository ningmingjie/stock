#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tushare as ts
import numpy as np
import pandas as pd
import redis

class Pierced:

    def __init__(self, ticker):
        self.ticker = ticker

    """
    获取历史行情数据
    startDay ：开始时间
    endDay ：结束时间
    """
    def getHistData(self, startDay = '2013-12-10', endDay = '2018-10-15'):
        data = ts.get_hist_data(self.ticker, startDay, endDay)
        data.reset_index(inplace=True)
        #索引重新命名
        data.rename(
            columns={'date': 'date', 'open': 'open', 'high': 'high', 'close': 'close', 'low': 'low', 'volume': 'volume',
                     'price_change': 'price_change', 'p_change': 'p_change', 'ma5': 'ma5', 'ma10': 'ma10',
                     'ma20': 'ma20', 'v_ma5': 'v_ma5', 'v_ma10': 'v_ma10', 'v_ma20': 'v_ma20'}, inplace=True)
        #返回字典类型
        return data.to_dict('records')

    def handel(self, startDay, endDay):
        #print self.ticker
        data = self.getHistData(startDay, endDay)
        dataLen = len(data)
        lst = []
        for i in range(dataLen-1, -1, -1):
            if data[i][3] > data[i][1]:
                continue
            if data[i][4] < data[i-1][1]:
                continue
            if data[i][1] < data[i-1][3]:
                continue
            average = (data[i][1]+data[i][3])/2
            if data[i-1][3] < average:
                continue
            lst.append([data[i][0], data[i-1][0]])
        if lst:
            return True
        else:
            return False

    def handelAll(self, startDay, endDay):
        #print self.ticker
        data = self.getHistData(startDay, endDay)
        dataLen = len(data)
        lst = []
        if data[1][3] > data[1][1]:
            return 0
        if data[1][4] < data[0][1]:
            return 0
        if data[1][1] < data[0][3]:
            return 0
        average = (data[1][1] + data[1][3]) / 2
        if data[0][3] < average:
            return 0
        lst.append([data[1][0], data[0][0]])
        if lst:
            return True
        else:
            return False

    def getTodayAll(self):
        data = ts.get_today_all()
        data.reset_index(inplace=True)
        dt = np.array(data)
        dts = dt.tolist()
        for st in dts:
            self.write(st[1])

    def write(self, ticker):
        fo = open("sk.txt", "a")
        fo.write(ticker + "\n")
        fo.close()
        return

class Stock:
    def getStockAll(self):
        with open('sk.txt', 'r') as f:
            lines = [line.strip() for line in f.readlines()]
        return lines

stock = Stock()
sk = stock.getStockAll()
result = []
for tk in sk:
    try:
        pierced = Pierced(tk)
        res = pierced.handelAll('2018-10-15', '2018-10-16')
        if res == True:
            print tk
            result.append(tk)
    except:
        continue
print result