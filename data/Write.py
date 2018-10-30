#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tushare as ts
import numpy as np
import pandas as pd

class Write:

    def __init__(self):
        self._path = "/data/share/loudou/stock/"

    def getTodayAll(self):
        data = ts.get_today_all()
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