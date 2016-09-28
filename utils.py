# coding:utf8
import time

class UtilsManager(object):

    #查看线路是否在运营时间内
    def checkWhetherOperating(self, line_info, stop_direction):
        # line_info是torndb.query返回的result

        # start_stop开始的stop_direction==1

        start_time = 0
        end_time = 0
        if stop_direction == 1:
            start_time = line_info['start_earlytime']
            end_time = line_info['start_latetime']
        else:
            start_time = line_info['end_earlytime']
            end_time = line_info['end_latetime']

        now_time = int(time.strftime("%H%M",time.localtime(time.time())))

        if now_time < start_time:
            return False

        if now_time > end_time:
            return False

        return True
