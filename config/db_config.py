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
        conn = False
        try:
            conn = MySQLdb.connect(
                host=self._dbhost,
                user=self._dbuser,
                passwd=self._dbpassword,
                db=self._dbname,
                port=self._dbport,
                cursorclass=MySQLdb.cursors.DictCursor,
                charset=self._dbcharset
            )
        except Exception, data:
            self._logger.error("connect database failed, %s" % data)
            conn = False
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
                self._logger.warn("query database exception, %s" % data)
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
                self._logger.warn("update database exception, %s" % data)

        return flag

    # 删除记录
    # 新增记录
    def insertData(self, sql):
        res = True
        if (self._conn):
            try:
                self._cursor.execute(sql)
            except Exception, data:
                res = False
                self._logger.warn("insert database exception, %s" % data)
        return res

    # 关闭数据库连接
    def close(self):
        if (self._conn):
            try:
                if (type(self._cursor) == 'object'):
                    self._cursor.close()
                if (type(self._conn) == 'object'):
                    self._conn.close()
            except Exception, data:
                self._logger.warn("close database exception, %s,%s,%s" % (data, type(self._cursor), type(self._conn)))

stock_db = DB(
    host="39.98.34.223",
    port=3306,
    db="stock",
    user="root",
    passwd="loudou123+",
    charset="utf-8"
)