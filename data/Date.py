#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import time


reload(sys)
sys.setdefaultencoding("utf-8")

class Date:

    def __init__(self):
        self._path = "/data/share/loudou/stock/"

    @staticmethod
    def getDateAmend(self, date):
        return time.strftime('%Y-%m-%d', time.strptime(date, "%Y%m%d"))