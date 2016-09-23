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

    print 'version=' + str(spiderMain.constants.pd_line_version)
    # app_modify
    spiderMain.parser.parserModify(spiderMain.url_modify)

    #
    print 'version3=' + str(spiderMain.constants.pd_line_version)

    print '完成'
