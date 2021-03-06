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

    # 插入线路的基本信息
    def insertLineInfo(self, line_id, line_name, start_stop, start_earlytime, start_latetime, end_stop, end_earlytime,
                       end_latetime, line_version, line_type):
        sql = "insert into t_line_info(line_id,line_name,start_stop,start_earlytime,start_latetime,end_stop,end_earlytime,end_latetime,line_version,line_type) values(%d,'%s','%s','%s','%s','%s','%s','%s',%d,%d)" % (
            line_id, line_name, start_stop, start_earlytime, start_latetime, end_stop, end_earlytime,
            end_latetime, line_version, line_type)

        result = self.db.insert(sql)
        return result

    # 插入站点信息
    def insertLineStop(self, line_id, stop_num, stop_direction, stop_name, stop_id, line_version, line_type):
        sql = "insert into t_line_stop(line_id,stop_num,stop_direction,stop_name,stop_id,line_version,line_type) values(%d,%d,%d,'%s','%s',%d,%d)" % (
            line_id, stop_num, stop_direction, stop_name, stop_id, line_version, line_type)

        result = self.db.insert(sql)
        return result

    # 查询t_line
    def getLines(self, line_name_pattern):
        sql = "select * from t_line where line_name like '" + line_name_pattern + "%%'"

        result = self.db.query(sql)
        return result

    # 查询一条线路的line_info
    def getLineInfo(self, line_name):
        sql = "select * from t_line_info where line_name = %s"

        result = self.db.get(sql, line_name)
        return result

    # 查看线路一个方向的所有站点
    def getLineStops(self, line_id, stop_direction):
        sql = "select * from t_line_stop where line_id = %d and stop_direction = %d order by stop_num" % (
            line_id, stop_direction)

        result = self.db.query(sql)
        return result

    # 插入线路时刻信息
    def insertLineTime(self, line_id, stop_id, stop_direction, log_time, car_info, stop_dis, distance, away_time):
        sql = "insert into t_line_time(line_id,stop_id,stop_direction,log_time,car_info,stop_dis,distance,away_time) values(%d,'%s',%d,%d,'%s',%d,%d,%d)" % (
            line_id, stop_id, stop_direction, log_time, car_info, stop_dis, distance, away_time)

        try:
            result = self.db.insert(sql)
            return result
        except Exception, e:
            print Exception, ":", e
            self.resetDB()

    def resetDB(self):
        self.db = torndb.Connection(
            host='mysql.t0.daoapp.io:61499',
            database='shjt_spider',
            user='root',
            password='xphone123',
            charset='utf8'
        )
