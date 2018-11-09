#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
sys.path.append('/data/www/stock/')
import tushare as ts
import numpy as np
import pandas as pd
import redis
import time
import re
from config.db_config import stock_db

reload(sys)
sys.setdefaultencoding('utf-8')

class History:

    def __init__(self, secCode, secName, secID):
        self.secCode = secCode
        self.secName = secName
        self.secID = secID

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
            print data[i-1]['date']


class Stock:
    def getStockAll(self):
        with open('/data/share/loudou/stock/stockTicker.txt', 'r') as f:
            lines = [line.strip() for line in f.readlines()]
        return lines

#stock = Stock()
#sk = stock.getStockAll()
sk = ["601518-吉林高速-601518.SH"]
for tk in sk:
    try:
        sec = re.split("-", tk)
        history = History(sec[0], sec[1], sec[2])
        res = history.handel('2016-01-01', '2018-10-30', 10)
        print sec[2]
    except Exception, data:
        print data