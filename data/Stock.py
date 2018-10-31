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

    def getTradeCal(self):
        pro = ts.pro_api()
        data = pro.trade_cal(exchange_id='', start_date=self._startDate, end_date=self._endDate)
        data.reset_index(inplace=True)
        print data.to_dict('records')