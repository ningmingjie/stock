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

class Stock:

    def __init__(self):
        self._startDate = time.strftime('%Y%m%d',time.localtime(time.time()-15*24*3600))
        self._endDate = time.strftime('%Y%m%d',time.localtime(time.time()))


    """
    获取交易列表
    """
    def getTradeCal(self):
        ts.set_token('9caf3d505f4f4b5cefd16f25c533e1cae081773442c216888678ddee')
        pro = ts.pro_api()
        data = pro.trade_cal(exchange_id='', start_date=self._startDate, end_date=self._endDate)
        data.reset_index(inplace=True)
        data = pd.DataFrame(data, columns=['is_open', 'cal_date'])
        print data.to_dict('records')

    """
    判断是否开盘
    secCode ：股票代码
    _date ：请求日期
    """
    def isOpen(self, secCode, _date):
        sk = ts.get_hist_data(secCode, _date, _date)
        sk.reset_index(inplace=True)
        if len(sk.to_dict('records')):
            return True

        return False




stock = Stock()
stock.getTradeCal()