# coding:utf-8
import json
import re
import time


class CLEAN_DATA:
    def __init__(self):
        self.data_list = []
    def get_Ua(self):
        with open('/share/home/wangjianxun/mobile_ua.txt', 'r') as f:
            all_content = f.readlines()
            print all_content[:10]

    def get_content(self):
        # with open('wangtest.txt','r') as f:
        with open('/data/var/log/catappitems_test1_log_2022_05_16_24_rproxy.log','r') as f:
            all_content = f.read()
            datalist = re.findall('seed:(.*?),items:', all_content)
            print "去重前 抓取数据：",len(datalist)*10
            d_count = 0
            for i in datalist:
                data_l = eval(i).get('pre_items')
                if data_l:
                    item_count = len(data_l)
                    d_count +=item_count
                    for d in data_l:
                        if d not in self.data_list:
                            self.data_list.append(d)

            # print self.data_list
            print "去重前 抓取数据：", d_count
            print "去重后 抓取数据：",len(self.data_list)

    def get_content2(self):
        # with open('wangtest.txt','r') as f:
        with open('content55.txt', 'r') as f:
            all_content = f.read()
            datalist = re.findall(',item_id:(.*?),price', all_content)
            d_count = len(datalist)
            for i in datalist:
                # print i
                if i not in self.data_list:
                    self.data_list.append(i)
                else:
                    print i
                    # print self.data_list
            print "去重前 抓取数据：", d_count
            print "去重后 抓取数据：",len(self.data_list)

    def get_content3(self):
        # with open('wangtest.txt','r') as f:
        with open('/data/test/catappitems_taobao_test0204_2022_05_23_24_rproxy.txt', 'r') as f:
        # with open('./123.txt', 'r') as f:
            all_content = f.read()
            datalist = re.findall('item_id": "(.*?)", "pro_price', all_content)
            d_count = len(datalist)
            for i in datalist:
                # print i
                if i not in self.data_list:
                    self.data_list.append(i)
                # else:
                #     print i
                    # print self.data_list
            print "去重前 抓取数据：", d_count
            print "去重后 抓取数据：",len(self.data_list)

clean_data = CLEAN_DATA()
# clean_data.get_content()
# clean_data.get_content2()
# clean_data.get_content3()
clean_data.get_Ua()

#worker starting
