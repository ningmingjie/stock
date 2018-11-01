#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tushare as ts
import numpy as np
import pandas as pd
import sys


reload(sys)
sys.setdefaultencoding("utf-8")

class Write:

    def __init__(self):
        self._path = "/data/share/loudou/stock/"
        ts.set_token('9caf3d505f4f4b5cefd16f25c533e1cae081773442c216888678ddee')

    def getTodayAll(self):
        #data = ts.get_today_all()
        pro = ts.pro_api()
        data = pro.query('stock_basic', exchange_id='', list_status='L',
                         fields='ts_code,symbol,name,area,industry,list_date')
        data.reset_index(inplace=True)
        dt = np.array(data)
        dts = dt.tolist()
        for st in dts:
            self.write(st[1], st[2])
        return True

    def write(self, secCode, secName):
        fo = open(self._path + "stockTicker.txt", "a")
        fo.write(secCode + "-" + secName + "\n")
        fo.close()
        return True

write = Write()
write.getTodayAll()