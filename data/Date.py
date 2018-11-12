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
    def getDateAmend(date):
        return time.strftime('%Y-%m-%d', time.strptime(date, "%Y%m%d"))

    @staticmethod
    def getDate(date):
        return time.strftime('%Y-%m-%d', time.strptime(date, "%Y-%m-%d %H:%M"))

    """
    格式化时间
    _date 时间
    format 时间格式
    expectFormat 期望得到的格式
    """
    @staticmethod
    def getDateFormat(_date, format, expectFormat):
        return time.strftime(expectFormat, time.strptime(_date, format))

    """
    获取N天前后的时间
    _date 时间
    _type 前后
    _number 天数
    format 时间格式
    expectFormat 期望得到的格式
    """
    @staticmethod
    def getDiffDate(_date, _number, _type = 'redu', expectFormat = '%Y%m%d', format = '%Y-%m-%d'):
        if _type == 'redu':
            return time.strftime(expectFormat,
                                 time.localtime(time.mktime(time.strptime(_date, format)) - _number * 24 * 3600))
        else:
            return time.strftime(expectFormat,
                                 time.localtime(time.mktime(time.strptime(_date, format)) + _number * 24 * 3600))