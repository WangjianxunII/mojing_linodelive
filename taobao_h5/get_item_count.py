# coding:utf-8
import re
class CLEAN_DATA:
    def __init__(self):
        self.data_list = []

    def get_content(self):
        # with open('wangtest.txt','r') as f:
        with open('/data/var/log/catappitems_test16_log_2022_05_10_24_rproxy.log','r') as f:
            all_content = f.read()
            datalist = re.findall('seed:(.*?),items:', all_content)
            print "去重前 抓取数据：",len(datalist)*10

clean_data = CLEAN_DATA()
clean_data.get_content()
