#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tushare as ts
import numpy as np
import pandas as pd

class Write:

    def getTodayAll(self):
        data = ts.get_today_all()
        data.reset_index(inplace=True)
        dt = np.array(data)
        dts = dt.tolist()
        for st in dts:
            self.write(st[1])
        return True

    def write(self, ticker):
        fo = open("stockTicker.txt", "a")
        fo.write(ticker + "\n")
        fo.close()
        return True