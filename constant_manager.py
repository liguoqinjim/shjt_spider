# coding:utf8

class ConstantsManager(object):
    def __init__(self):
        self.app_version = 0
        self.pd_line_version = 0
        self.px_line_version = 0

        # px_line=1,pd_line=2
        self.LINE_TYPE_PX = 1
        self.LINE_TYPE_PD = 2

        self.px_lines = None
        self.pd_lines = None
        self.pd_line_url = ""
        self.px_line_url = ""
        self.pd_get_line_info_by_name_url = ""
        self.px_get_line_info_by_name_url = ""
        self.pd_get_line = ""
        self.px_get_line = ""
        self.pd_car_monitor = ""
        self.px_car_monitor = ""
        self.px_get_dispatch_screen = ""
        self.pd_get_dispatch_screen = ""
        self.px_code = ""
        self.pd_code = ""

    '''
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
            <code px="VvXWg1DSOPETgNXzVyjzgc==" pd="PmDDkyguobXrMWIsD1IBqVXEWv0="/>'''

