#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import tushare as ts
import pandas as pd
import time

reload(sys)
sys.setdefaultencoding('utf-8')

class Stock:

    def __init__(self, number = 7):
        ts.set_token('9caf3d505f4f4b5cefd16f25c533e1cae081773442c216888678ddee')
        self._startDate = time.strftime('%Y%m%d',time.localtime(time.time()-number*24*3600))
        self._endDate = time.strftime('%Y%m%d',time.localtime(time.time()))


    """
    获取当天是否是交易日
    """
    def getTodayTradeCal(self):
        pro = ts.pro_api()
        data = pro.trade_cal(exchange_id='', start_date=self._endDate, end_date=self._endDate)
        data.reset_index(inplace=True)
        data = pd.DataFrame(data, columns=['is_open', 'cal_date'])
        if data.to_dict('records')[0]['is_open']:
            return True
        return False

    """
    获取交易列表
    """
    def getTradeCalList(self, startDate, endDate):
        pro = ts.pro_api()
        data = pro.trade_cal(exchange_id='', start_date=startDate, end_date=endDate)
        data.reset_index(inplace=True)
        data = pd.DataFrame(data, columns=['is_open', 'cal_date'])
        print data.to_dict('records')

    """
    获取某只股票的上个交易日
    secCode ：股票代码
    _date ：请求日期
    """
    def getLastTradeCal(self, secCode):
        sk = ts.get_hist_data(secCode)
        sk.reset_index(inplace=True)
        if len(sk.to_dict('records')):
            return True

        return False

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

    """
    获取日行情数据
    startDay ：开始时间
    endDay ：结束时间
    """
    def getHistData(self, secCode, startDate, endDate):
        data = ts.get_hist_data(secCode, startDate, endDate)
        data.reset_index(inplace=True)
        #索引重新命名
        data.rename(
            columns={'date': 'date', 'open': 'open', 'high': 'high', 'close': 'close', 'low': 'low', 'volume': 'volume',
                     'price_change': 'price_change', 'p_change': 'p_change', 'ma5': 'ma5', 'ma10': 'ma10',
                     'ma20': 'ma20', 'v_ma5': 'v_ma5', 'v_ma10': 'v_ma10', 'v_ma20': 'v_ma20'}, inplace=True)
        #返回字典类型
        return data.to_dict('records')

    def getSuspend(self):
        pro = ts.pro_api()
        #df = pro.query('suspend', ts_code='', suspend_date=self._endDate, resume_date='', fiedls='')
        df = pro.suspend(ts_code='000972.SZ', suspend_date='', resume_date='', fiedls='')
        print df


stock = Stock()
stock.getSuspend()
#stock.getTradeCalList('20181031', '20181101')