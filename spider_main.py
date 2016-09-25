# coding:utf8
import response_parser
import constant_manager


class SpiderMain(object):
    def __init__(self):
        self.url_version = 'http://www.jt.sh.cn/trafficWeb/lbs/shjtmap.xml'
        self.url_modify = 'http://www.jt.sh.cn/trafficWeb/lbs/modify.xml'

        self.constants = constant_manager.ConstantsManager()
        self.parser = response_parser.ResponseParser(self.constants)


if __name__ == '__main__':
    spiderMain = SpiderMain()

    # app_version
    app_version = spiderMain.parser.parseVersion(spiderMain.url_version)
    spiderMain.constants.app_version = app_version

    # app_modify
    spiderMain.parser.parserModify(spiderMain.url_modify)

    #
    print "解析"
    '''
<linedetails><linedetail><end_earlytime>05:30</end_earlytime><end_latetime>22:30</end_latetime><end_stop>龙阳路地铁站</end_stop><line_id>10465</line_id><line_name>976路</line_name><start_earlytime>05:30</start_earlytime><start_latetime>22:30</start_latetime><start_stop>上浦路济阳路</start_stop></linedetail></linedetails>
    '''

    # 先只分析浦东
    if spiderMain.constants.pd_lines == None:
        # 分析线路信息
        spiderMain.parser.parseLine(spiderMain.constants.pd_line_version, spiderMain.constants.LINE_TYPE_PD,
                                    spiderMain.constants.pd_line_url, False)

        # 分析线路站点
        spiderMain.parser.parseLineStops(spiderMain.constants.pd_line_version, spiderMain.constants.LINE_TYPE_PD)

    # print len(spiderMain.constants.pd_lines)
    # spiderMain.parser.parseLineInfo(spiderMain.constants.pd_line_version, spiderMain.constants.LINE_TYPE_PD,
    #                                 spiderMain.constants.pd_get_line_info_by_name_url, False)

    print '完成'
