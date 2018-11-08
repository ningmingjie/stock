#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import re
import sys
sys.path.append('/data/www/stock/')
import time
from data.Stock import Stock
from config.db_config import stock_db
from data.Date import Date

from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')

class Suspen:

    def __init__(self):
        self.headers = {'content-type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
        self._date = time.strftime('%Y-%m-%d',time.localtime(time.time()))

    def getSoup(self, page):
        response = requests.get(
            url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=FD&sty=SRB&st=0&sr=-1&p=%d&ps=50&js=var%%20RxRHbeMB={pages:(pc),data:[(x)]}&mkt=1&fd=%s&rt=51383288" % (page, self._date),
            headers = self.headers
        )
        return BeautifulSoup(response.text, features='lxml')

    def getData(self):
        data = self.getSoup(1)
        pattern = re.compile(r'[[](.*?)[]]', re.S)
        data = re.findall(pattern, bytes(data))
        if len(data) == 0:
            return True
        pattern = re.compile(r'"(.*?)"', re.S)
        data = re.findall(pattern, data[0])
        for i in range(len(data)):
            val = re.split(",", data[i])
            self.insertData(val)

    def insertData(self, query):
        stock = Stock.getCodeStockInfo(query[0])
        if stock == None:
            return False
        sql = """INSERT INTO suspend (sec_id, sec_code, sec_name, suspend_type, suspend_date, suspend_reason, created_at, updated_at) VALUES ('%s', '%s', '%s', '%d', '%s', \
'%s', '%d', '%d')""" % (stock['sec_id'], stock['sec_code'], stock['sec_name'], 10, Date.getDate(query[2]), query[5], int(time.time()), int(time.time()))
        stock_db.insertData(sql)


suspen = Suspen()
suspen.getData()
