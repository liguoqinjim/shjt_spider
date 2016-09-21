# coding:utf8
import torndb
import json
import time


class DBManager(object):
    def __init__(self):
        self.db = torndb.Connection(
            host='mysql.t0.daoapp.io:61499',
            database='shjt_spider',
            user='root',
            password='xphone123',
            charset='utf8'
        )

    # 得到现在的系统版本号
    def getCurrentVersion(self):
        sql = 'select * from t_version order by id desc limit 1'
        result = self.db.get(sql)
        if result == None:
            return 0
        # print result['version']
        return result['version']

    # 当app版本更新的时候和系统现在版本不一致的时候，记录到表中
    def insertVersion(self, version):
        sql = 'insert into t_version(version,version_time) values(%d,%d)' % (version, time.time())
        result = self.db.insert(sql)

        return result

    # 得到线路的版本
    def getCurrentLineVersion(self, line_type):
        sql = 'select * from t_line_version where line_type = %d order by id desc limit 1' % line_type
        result = self.db.get(sql)

        if result == None:
            return 0

        return result['line_version']

    # 插入线路的版本
    def insertLineVersion(self, line_type, line_version):
        sql = 'insert into t_line_version(line_type,line_version,version_time) values(%d,%d,%d)' % (
            line_type, line_version, time.time())
        result = self.db.insert(sql)

        return result

    # 插入线路
    def insertLine(self, line_version, line_type, line_name, line_actual):
        sql = "insert into t_line(line_version,line_type,line_name,line_actual,line_time) values(%d,%d,'%s','%s',%d)" % (
            line_version, line_type, line_name, line_actual, time.time())

        result = self.db.insert(sql)

        return result
