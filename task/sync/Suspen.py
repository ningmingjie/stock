#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import re
import sys
import MySQLdb
import time

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
            url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=FD&sty=SRB&st=0&sr=-1&p='%d'&ps=50&js=var%%20RxRHbeMB={pages:(pc),data:[(x)]}&mkt=1&fd='%s'&rt=51383288" % (page, self._date),
            headers = self.headers
        )
        return BeautifulSoup(response.text, features='lxml')

    def getData(self):
        data = self.getSoup(1)
        print data


suspen = Suspen()
suspen.getData()
