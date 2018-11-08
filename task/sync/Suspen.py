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

    #获取东财停复牌数据
    def getSoup(self, page):
        response = requests.get(
            url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=FD&sty=SRB&st=0&sr=-1&p=%d&ps=50&js=var%%20RxRHbeMB={pages:(pc),data:[(x)]}&mkt=1&fd=%s&rt=51383288" % (page, self._date),
            headers = self.headers
        )
        return BeautifulSoup(response.text, features='lxml')

    #数据处理
    def getData(self, page):
        data = self.getSoup(page)
        pattern = re.compile(r'[[](.*?)[]]', re.S)
        data = re.findall(pattern, bytes(data))
        if len(data) == 0:
            return False
        pattern = re.compile(r'"(.*?)"', re.S)
        data = re.findall(pattern, data[0])
        sqlUp = """UPDATE suspend SET suspend_type = '%d'""" % (30)
        stock_db.update(sqlUp)
        for i in range(len(data)):
            val = re.split(",", data[i])
            stock = Stock.getCodeStockInfo(val[0])
            if stock == None:
                continue
            reSql = """SELECT * FROM suspend WHERE sec_code = '%s' AND suspend_date = '%s'""" % (stock['sec_code'], Date.getDate(val[2]))
            query = stock_db.fetch_one(reSql)
            if query != None:
                upSql = """UPDATE suspend SET suspend_type = '%d'  WHERE sec_code = '%s' AND suspend_date = '%s'""" % (10, stock['sec_code'], Date.getDate(val[2]))
                stock_db.update(upSql)
                continue
            sql = """INSERT INTO suspend (sec_id, sec_code, sec_name, suspend_type, suspend_date, suspend_reason, created_at, updated_at) VALUES ('%s', '%s', '%s', '%d', '%s', \
'%s', '%d', '%d')""" % (stock['sec_id'], stock['sec_code'], stock['sec_name'], 10, Date.getDate(val[2]), val[5],int(time.time()), int(time.time()))
            stock_db.insertData(sql)
        return True

suspen = Suspen()
for i in range(1, 10):
    res = suspen.getData(i)
    if res == False:
        exit()
