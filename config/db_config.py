# encoding:utf-8
# name:mod_db.py

import MySQLdb
import MySQLdb.cursors
#import mod_config
#import mod_logger

#LOGPATH = mod_config.getConfig('path', 'logpath') + 'database.log'
#logger = mod_logger.logger(LOGPATH)

# 数据库操作类
class DB(object):
    # 初始化
    def __init__(self, host, port, db, user, passwd, charset):
        #self._logger = logger
        self._dbname = db
        self._dbhost = host
        self._dbport = int(port)
        self._dbuser = user
        self._dbpassword = passwd
        self._dbcharset = charset

        self._conn = self.connectMySQL()



        if (self._conn):
            self._cursor = self._conn.cursor()


    # 数据库连接
    def connectMySQL(self):
        conn = MySQLdb.connect(
            host=self._dbhost,
            db=self._dbname,
            user=self._dbuser,
            passwd=self._dbpassword,
            port=self._dbport,
            charset=self._dbcharset
        )

        return conn

    # 获取查询结果集
    def fetch_all(self, sql):
        res = ''
        if (self._conn):
            try:
                self._cursor.execute(sql)
                res = self._cursor.fetchall()
            except Exception, data:
                res = False
                #self._logger.warn("query database exception, %s" % data)
        return res
    # 更新数据
    def update(self, sql):
        flag = False
        if (self._conn):
            try:
                self._cursor.execute(sql)
                self._conn.commit()
                flag = True
            except Exception, data:
                flag = False
                #self._logger.warn("update database exception, %s" % data)

        return flag

    # 删除记录
    # 新增记录
    def insertData(self, sql):
        id = 0
        if (self._conn):
            try:
                self._cursor.execute(sql)
                self._conn.commit()
                id = int(self._conn.lastrowid())
            except Exception, data:
                self._conn.rollback()
                #self._logger.warn("insert database exception, %s" % data)
        return id

    # 关闭数据库连接
    def close(self):
        if (self._conn):
            try:
                if (type(self._cursor) == 'object'):
                    self._cursor.close()
                if (type(self._conn) == 'object'):
                    self._conn.close()
            except Exception, data:
                return False

stock_db = DB(
    host="172.26.202.108",
    port=3306,
    db="stock",
    user="stock",
    passwd="loudou123~",
    charset="utf8"
)