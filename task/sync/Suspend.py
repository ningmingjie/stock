#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
sys.path.append('/data/www/stock/')
import tushare as ts
import pandas as pd
import time
import re
from config.db_config import stock_db
from data import Date

reload(sys)
sys.setdefaultencoding('utf-8')

class Suspend:
    #10:停牌
    #20:复牌
    def __init__(self, secCode, secName):
        ts.set_token('9caf3d505f4f4b5cefd16f25c533e1cae081773442c216888678ddee')
        self._endDate = time.strftime('%Y%m%d',time.localtime(time.time()))
        self.secCode = secCode
        self.secName = secName

    #获取停复牌信息
    def getSuspend(self, secID):
        pro = ts.pro_api()
        data = pro.suspend(ts_code=secID, suspend_date='', resume_date='', fiedls='')
        return data.to_dict('records')[0]

    #写入数据
    def insertSuspend(self, secID):
        suspend = self.getSuspend(secID)
        _date = Date.getDateAmend()
        print _date
        #sql = """INSERT INTO suspend (sec_id, sec_code, sec_name, suspend_type, suspend_date, suspend_reason, created_at, updated_at) VALUES ('%s', '%s', \
#'%s', '%d', '%s', '%s', '%d', '%d')""" % (secID, self.secCode, self.secName, 10, 1, suspend['suspend_reason'], int(time.time()), int(time.time()))

        #stock_db.insertData(sql)


class getStock:
    def getStockAll(self):
        with open('/data/share/loudou/stock/stockTicker.txt', 'r') as f:
            lines = [line.strip() for line in f.readlines()]
        return lines


#stock = getStock()
#sk = stock.getStockAll()
sk = ["603990-麦迪科技-603990.SH"]
for tk in sk:
    sec = re.split("[-]", tk)
    suspend = Suspend()
    suspend.insertSuspend(sec[2])
#stock = Stock()
#stock.getSuspend()
#stock.getTradeCalList('20181031', '20181101')