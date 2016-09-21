# coding:utf8
import requests
from lxml import etree

from db_manager import DBManager
from constant_manager import ConstantsManager


class ResponseParser(object):
    def __init__(self):
        self.dbMandger = DBManager()
        self.constantsUtil = ConstantsManager()

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
        pd_line_url = root.xpath('/modify/pd_line/@url')[0]
        px_line_url = root.xpath('/modify/px_line/@url')[0]

        # 浦西
        current_px_version = self.dbMandger.getCurrentLineVersion(self.constantsUtil.LINE_TYPE_PX)
        self.constantsUtil.px_line_version = px_line_version
        if current_px_version != px_line_version:
            print '浦西线路更新'

            self.constantsUtil.px_line_version = px_line_version

            self.dbMandger.insertLineVersion(self.constantsUtil.LINE_TYPE_PX, px_line_version)

            # 插入新的路线
            self.parseLine(px_line_version, self.constantsUtil.LINE_TYPE_PX, px_line_url)

            print '浦西线路更新完成'

        # 浦东
        current_pd_version = self.dbMandger.getCurrentLineVersion(self.constantsUtil.LINE_TYPE_PD)
        self.constantsUtil.pd_line_version = current_pd_version
        if current_pd_version != pd_line_version:
            print '浦东线路更新'
            print pd_line_url
            self.constantsUtil.pd_line_version = pd_line_version

            self.dbMandger.insertLineVersion(self.constantsUtil.LINE_TYPE_PD, pd_line_version)

            # 插入新的线路
            self.parseLine(pd_line_version, self.constantsUtil.LINE_TYPE_PD, pd_line_url)
            print '浦东线路更新完成'

    def parseLine(self, line_version, line_type, url):
        response = requests.get(url).content

        root = etree.XML(response)

        '''
            <lines version="32">
                <line name="11路" actual="11"/>
        '''
        lines = root.xpath('/lines/line')

        for line in lines:
            name = line.xpath('@name')[0]
            actual = ""
            if line_type == self.constantsUtil.LINE_TYPE_PX:
                actual = line.xpath('@actual')[0]

            self.dbMandger.insertLine(line_version, line_type, name, actual)
