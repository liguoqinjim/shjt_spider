# coding:utf8

class ConstantsManager(object):
    def __init__(self):
        self.app_version = 0
        self.pd_line_version = 0
        self.px_line_version = 0

        # px_line=1,pd_line=2
        self.LINE_TYPE_PX = 1
        self.LINE_TYPE_PD = 2
