# coding:utf8
import response_parser
import constant_manager
import db_manager
import utils
import threading
import time


class SpiderMain(object):
    def __init__(self):
        self.url_version = 'http://www.jt.sh.cn/trafficWeb/lbs/shjtmap.xml'
        self.url_modify = 'http://www.jt.sh.cn/trafficWeb/lbs/modify.xml'

        self.utils = utils.UtilsManager()
        self.constants = constant_manager.ConstantsManager()
        self.db = db_manager.DBManager()
        self.parser = response_parser.ResponseParser(self.constants, self.db)


if __name__ == '__main__':
    spiderMain = SpiderMain()

    # app_version
    app_version = spiderMain.parser.parseVersion(spiderMain.url_version)
    spiderMain.constants.app_version = app_version

    # app_modify
    spiderMain.parser.parserModify(spiderMain.url_modify)

    #
    print "解析"

    # 先只分析浦东
    # if spiderMain.constants.pd_lines == None:
    # 分析线路信息
    # spiderMain.parser.parseLine(spiderMain.constants.pd_line_version, spiderMain.constants.LINE_TYPE_PD,
    #                             spiderMain.constants.pd_line_url, False)

    # 分析线路站点
    # spiderMain.parser.parseLineStops(spiderMain.constants.pd_line_version, spiderMain.constants.LINE_TYPE_PD)


    # 分析871
    myLineName = '871'
    resultLine = spiderMain.db.getLines(myLineName)
    for r in resultLine:
        if myLineName in str(r["line_name"]):  # 查询到
            resultLineInfo = spiderMain.db.getLineInfo(r["line_name"])

            #判断是不是在运营时间里面
            # operating = spiderMain.utils.checkWhetherOperating(resultLineInfo,1)
            # if operating:
            #     print '在运营时间内' + str(time.time())
            # else:
            #     print '不在运营时间内' + str(time.time())
            # operating = spiderMain.utils.checkWhetherOperating(resultLineInfo, 2)

            line_id = int(resultLineInfo["line_id"])

            stop1 = spiderMain.db.getLineStops(line_id, 1)
            stop2 = spiderMain.db.getLineStops(line_id, 2)

            n = 0
            while True:

                #判断stop_direction==1的是否在运营时间内
                operating = spiderMain.utils.checkWhetherOperating(resultLineInfo, 1)
                if operating:
                    for stop in stop1:
                        stop_id = str(stop["stop_id"])
                        line_id = int(str(stop["line_id"]))
                        spiderMain.parser.parseLineTime(line_id, stop_id, 1, spiderMain.constants.LINE_TYPE_PD)
                        n += 1
                        if n % 10 == 0:
                            print '现在已经收集' + str(n) + "条记录"
                        time.sleep(5)
                else:
                    time.sleep(3600)
                    print '不在运营时间内' + str(time.time())

                #判断stop_direction==2的是否在运营时间内
                operating = spiderMain.utils.checkWhetherOperating(resultLineInfo, 2)
                if operating:
                    for stop in stop2:
                        stop_id = str(stop["stop_id"])
                        line_id = int(str(stop["line_id"]))
                        spiderMain.parser.parseLineTime(line_id, stop_id, 2, spiderMain.constants.LINE_TYPE_PD)
                        n += 1
                        if n % 10 == 0:
                            print '现在已经收集' + str(n) + "条记录"
                        time.sleep(5)
                else:
                    time.sleep(3600)
                    print '不在运营时间内' + str(time.time())



    # spiderMain.parser.parseLineTime(10407, 1837039618, 1, spiderMain.constants.LINE_TYPE_PD)

    print '完成'
