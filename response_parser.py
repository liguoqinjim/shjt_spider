# coding:utf8
import requests
from lxml import etree

from db_manager import DBManager


class ResponseParser(object):
    def __init__(self):
        self.dbMandger = DBManager()

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

        version = root.xpath('/update/version/text()')[0]
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

        pd_line_version = root.xpath('/modify/pd_line/@version')[0]
        px_line_version = root.xpath('/modify/px_line/@version')[0]
        pd_line_url = root.xpath('/modify/pd_line/@url')[0]
        px_line_url = root.xpath('/modify/px_line/@url')[0]

