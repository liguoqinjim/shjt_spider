# coding:utf8
import requests
import time
from lxml import etree

import sys;

reload(sys);
sys.setdefaultencoding("utf8")

from db_manager import DBManager
from constant_manager import ConstantsManager


class ResponseParser(object):
    def __init__(self, constant, db):
        self.dbMandger = db
        # self.constantsUtil = ConstantsManager()
        self.constantsUtil = constant

    # 解析当前版本号
    def parseVersion(self, url):
        '''
        <update>
            <version>67</version>
            <apk>http://www.jt.sh.cn/trafficWeb/lbs/shjtmap.apk</apk>
        </update>
        '''
        response = requests.get(url).text
        # xml = bytes(bytearray(xml, encoding='utf-8'))
        response = bytes(bytearray(response, encoding='utf-8'))

        # parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        # root = etree.fromstring(response, parser)
        # print response
        root = etree.XML(response)

        version = int(str(root.xpath('/update/version/text()')[0]))
        apk_url = root.xpath('/update/apk/text()')[0]

        current_version = self.dbMandger.getCurrentVersion()
        if current_version != version:
            self.dbMandger.insertVersion(int(str(version)))

        return version

    # 解析各个链接的变化
    def parserModify(self, url):
        '''
        <modify>
            <pd_get_line_info_by_name url="http://180.166.5.82:8000/palmbus_serv/PalmBusJgj/getLineInfoByName.do"/>
            <px_get_line_info_by_name url="http://bst.shdzyb.com:36001/Project/Ver2/getLineInfoByName.ashx"/>
            <pd_get_line url="http://180.166.5.82:8000/palmbus_serv/PalmBusJgj/getLine.do"/>
            <px_get_line url="http://bst.shdzyb.com:36001/Project/Ver2/getLine.ashx"/>
            <pd_car_monitor url="http://180.166.5.82:8000/palmbus_serv/PalmBusJgj/carMonitor.do"/>
            <px_car_monitor url="http://bst.shdzyb.com:36001/Project/Ver2/carMonitor.ashx"/>
            <px_get_dispatch_screen url="http://bst.shdzyb.com:36001/Project/Ver2/getdispatchScreen.ashx"/>
            <pd_get_dispatch_screen url="http://180.166.5.82:8000/palmbus_serv/PalmBusJgj/getdispatchScreen.do"/>
            <pd_line version="21" url="http://www.jt.sh.cn/trafficWeb/lbs/pd.xml"/>
            <px_line version="32" url="http://www.jt.sh.cn/trafficWeb/lbs/px.xml"/>
            <bulletin version="12" url="http://www.jt.sh.cn/trafficWeb/lbs/bulletin.xml"/>
            <metro version="8" url="http://218.242.181.87:8090/metro.zip"/>
            <data version="2" url="http://www.jt.sh.cn/trafficWeb/lbs/data.zip"/>
            <code px="VvXWg1DSOPETgNXzVyjzgc==" pd="PmDDkyguobXrMWIsD1IBqVXEWv0="/>
        </modify>
        '''

        response = requests.get(url).text
        response = bytes(bytearray(response, encoding='utf-8'))
        root = etree.XML(response)

        pd_line_version = int(str(root.xpath('/modify/pd_line/@version')[0]))
        px_line_version = int(str(root.xpath('/modify/px_line/@version')[0]))
        pd_line_url = str(root.xpath('/modify/pd_line/@url')[0])
        px_line_url = str(root.xpath('/modify/px_line/@url')[0])
        self.constantsUtil.pd_line_url = pd_line_url
        self.constantsUtil.px_line_url = px_line_url

        pd_get_line_info_by_name_url = str(root.xpath('/modify/pd_get_line_info_by_name/@url')[0])
        px_get_line_info_by_name_url = str(root.xpath('/modify/px_get_line_info_by_name/@url')[0])
        self.constantsUtil.pd_get_line_info_by_name_url = pd_get_line_info_by_name_url
        self.constantsUtil.px_get_line_info_by_name_url = px_get_line_info_by_name_url

        pd_get_line_url = str(root.xpath('/modify/pd_get_line/@url')[0])
        px_get_line_url = str(root.xpath('/modify/px_get_line/@url')[0])
        self.constantsUtil.pd_get_line_url = pd_get_line_url
        self.constantsUtil.px_get_line_url = px_get_line_url

        pd_car_monitor_url = str(root.xpath('/modify/pd_car_monitor/@url')[0])
        px_car_monitor_url = str(root.xpath('/modify/px_car_monitor/@url')[0])
        self.constantsUtil.pd_car_monitor_url = pd_car_monitor_url
        self.constantsUtil.px_car_monitor_url = px_car_monitor_url

        # 浦西
        current_px_version = self.dbMandger.getCurrentLineVersion(self.constantsUtil.LINE_TYPE_PX)
        self.constantsUtil.px_line_version = px_line_version
        if current_px_version != px_line_version:
            print '浦西线路更新'

            self.constantsUtil.px_line_version = px_line_version

            self.dbMandger.insertLineVersion(self.constantsUtil.LINE_TYPE_PX, px_line_version)

            # 插入新的路线
            self.parseLine(px_line_version, self.constantsUtil.LINE_TYPE_PX, px_line_url, True)

            print '浦西线路更新完成'

        # 浦东
        current_pd_version = self.dbMandger.getCurrentLineVersion(self.constantsUtil.LINE_TYPE_PD)
        self.constantsUtil.pd_line_version = current_pd_version
        print 'version2=' + str(self.constantsUtil.pd_line_version)
        if current_pd_version != pd_line_version:
            print '浦东线路更新'
            print pd_line_url
            self.constantsUtil.pd_line_version = pd_line_version

            self.dbMandger.insertLineVersion(self.constantsUtil.LINE_TYPE_PD, pd_line_version)

            # 插入新的线路
            self.parseLine(pd_line_version, self.constantsUtil.LINE_TYPE_PD, pd_line_url, True)
            print '浦东线路更新完成'

    def parseLine(self, line_version, line_type, url, whether_db):
        response = requests.get(url).content

        root = etree.XML(response)

        '''
            <lines version="32">
                <line name="11路" actual="11"/>
        '''
        lines = root.xpath('/lines/line')

        if line_type == self.constantsUtil.LINE_TYPE_PX:
            self.constantsUtil.px_lines = lines

        if line_type == self.constantsUtil.LINE_TYPE_PD:
            self.constantsUtil.pd_lines = lines

        for line in lines:
            name = line.xpath('@name')[0]
            actual = ""
            if line_type == self.constantsUtil.LINE_TYPE_PX:
                actual = line.xpath('@actual')[0]

            if whether_db:
                self.dbMandger.insertLine(line_version, line_type, name, actual)

    def parseLineInfo(self, line_version, line_type, url, whether_db):
        lines = None
        if line_type == self.constantsUtil.LINE_TYPE_PD:
            lines = self.constantsUtil.pd_lines
        else:
            lines = self.constantsUtil.px_lines

        for line in lines:
            name = line.xpath('@name')[0]
            actual = ""
            if line_type == self.constantsUtil.LINE_TYPE_PX:
                actual = line.xpath('@actual')[0]

            # 浦东
            if line_type == self.constantsUtil.LINE_TYPE_PD:
                final_url = url + '?linename=' + name
                # print final_url

                response = requests.get(final_url).content

                # print response
                '''<linedetails><linedetail><end_earlytime>05:30</end_earlytime><end_latetime>23:00</end_latetime><end_stop>齐河路云莲路</end_stop><line_id>10103</line_id><line_name>119路</line_name><start_earlytime>05:00</start_earlytime><start_latetime>23:00</start_latetime><start_stop>泰东路渡口</start_stop></linedetail></linedetails>'''

                root = etree.XML(response)
                line_list = root.xpath("/linedetails/linedetail/line_id/text()")
                line_id = 0
                line_name = ""
                start_stop = ""
                start_earlytime = ""
                start_latetime = ""
                end_stop = ""
                end_earlytime = ""
                end_latetime = ""
                if len(line_list) > 0:
                    line_id = int(str(line_list[0]))
                    line_name = str(root.xpath("/linedetails/linedetail/line_name/text()")[0])
                    # print line_name
                    start_stop = str(root.xpath("/linedetails/linedetail/start_stop/text()")[0])
                    start_earlytime = str(root.xpath("/linedetails/linedetail/start_earlytime/text()")[0])
                    start_latetime = str(root.xpath("/linedetails/linedetail/start_latetime/text()")[0])
                    # print start_stop + "|" + start_earlytime + "|" + start_latetime
                    end_stop = str(root.xpath("/linedetails/linedetail/end_stop/text()")[0])
                    end_earlytime = str(root.xpath("/linedetails/linedetail/end_earlytime/text()")[0])
                    end_latetime = str(root.xpath("/linedetails/linedetail/end_latetime/text()")[0])
                    # print end_stop + "|" + end_earlytime + "|" + end_latetime

                # print "line_id="
                # print line_id
                # if line_id == 0:



                if line_id != 0:
                    if whether_db == True:
                        print '插入数据库'
                        self.dbMandger.insertLineInfo(line_id, line_name, start_stop, start_earlytime, start_latetime,
                                                      end_stop, end_earlytime, end_latetime, line_version, line_type)

    def parseLineInfoId(self, line_type, line_name):
        url = ''
        if line_type == self.constantsUtil.LINE_TYPE_PD:
            url = self.constantsUtil.pd_get_line_info_by_name_url
        else:
            url = self.constantsUtil.px_get_line_info_by_name_url

        final_url = ''
        if line_type == self.constantsUtil.LINE_TYPE_PD:
            final_url = url + '?linename=' + line_name
        else:
            print '浦西'

        response = requests.get(final_url).content
        root = etree.XML(response)
        line_list = root.xpath("/linedetails/linedetail/line_id/text()")
        line_id = 0
        if len(line_list) > 0:
            line_id = int(str(line_list[0]))

        return line_id

    def parseLineStop(self, line_version, line_type, line_id):
        url = ""
        final_url = ""
        if line_type == self.constantsUtil.LINE_TYPE_PD:
            url = self.constantsUtil.pd_get_line_url
            final_url = url + "?lineid=" + str(line_id)
        else:
            url = self.constantsUtil.px_get_line_url

        response = requests.get(final_url).content
        # print response
        root = etree.XML(response)

        result0s = root.xpath('/lineInfoDetails/lineResults0/stop')
        result1s = root.xpath('/lineInfoDetails/lineResults1/stop')

        # print result0s

        stop_num1 = 1
        for result0 in result0s:
            stop_name = str(result0.xpath("zdmc/text()")[0])
            stop_id = int(str(result0.xpath("id/text()")[0]))
            # print 'stop_name=' + stop_name + ' | stop_id=' + str(stop_id)
            # result0的stop_direction填1
            self.dbMandger.insertLineStop(line_id, stop_num1, 1, stop_name, stop_id, line_version, line_type)
            stop_num1 += 1

        stop_num2 = 1
        for result1 in result1s:
            stop_name = str(result1.xpath("zdmc/text()")[0])
            stop_id = int(str(result1.xpath("id/text()")[0]))
            # result1的stop_direction填2
            self.dbMandger.insertLineStop(line_id, stop_num2, 2, stop_name, stop_id, line_version, line_type)
            stop_num2 += 1

    def parseLineStops(self, line_version, line_type):
        lines = None
        if line_type == self.constantsUtil.LINE_TYPE_PD:
            lines = self.constantsUtil.pd_lines
        else:
            lines = self.constantsUtil.px_lines

        n = 0
        for line in lines:
            name = line.xpath('@name')[0]

            # 浦东

            if line_type == self.constantsUtil.LINE_TYPE_PD:
                line_id = self.parseLineInfoId(line_type, name)
                print '解析线路' + str(line_id)
                if line_id != 0:
                    self.parseLineStop(line_version, line_type, line_id)

                n += 1
                print '解析完成度=' + str(n) + "/" + str(len(lines))

    # 解析线路时刻
    def parseLineTime(self, line_id, stop_id, stop_direction, line_type):
        # line_type判断用哪个url
        final_url = ""
        if line_type == self.constantsUtil.LINE_TYPE_PD:
            url = self.constantsUtil.pd_car_monitor_url
            final_url = url + "?lineid=" + str(line_id) + "&stopid=" + str(stop_id) + "&direction=" + str(
                stop_direction)
        else:
            # 浦西暂时不做
            url = self.constantsUtil.px_car_monitor_url

        log_time = time.time()
        # print final_url
        response = requests.get(final_url).content
        root = etree.XML(response)

        cars = root.xpath("/result/cars/car")

        # print response

        for car in cars:
            terminal = str(car.xpath("terminal/text()")[0])
            stopdis = int(str(car.xpath("stopdis/text()")[0]))
            distance = int(str(car.xpath("distance/text()")[0]))
            away_time = str(car.xpath("time/text()")[0])
            if '分钟' in away_time:  # 可以会出现25分钟以上，这种选项
                away_time = 99999
            else:
                away_time = int(away_time)

            self.dbMandger.insertLineTime(line_id, stop_id, stop_direction, log_time, terminal, stopdis, distance,
                                          away_time)
