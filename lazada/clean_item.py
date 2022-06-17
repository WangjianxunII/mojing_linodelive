# coding:utf-8
import json
import random
import re
import time


class CLEAN_DATA:
    def __init__(self):
        self.data_list = []
    def get_Ua(self):
        with open('/share/home/wangjianxun/mobile_ua.txt', 'r') as f:
            UALIST = f.readlines()
            # print len(UALIST)
            # useragent = random.choice(UALIST)
            # print useragent.strip()
            return UALIST

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
        with open('content44.txt', 'r') as f:
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
        # with open('/data/lazada_sg/lazada_sg__2022_06_13_1_rproxy.txt', 'r') as f1:
        with open('./data1.txt', 'r') as f1:
            all_content1 = f1.read()
        # with open('/data/lazada_sg/lazada_sg__2022_06_13_2_rproxy.txt', 'r') as f2:
        with open('./data2.txt', 'r') as f2:
            all_content2 = f2.read()
        all_content = all_content1+all_content2
        print len(all_content)
        datalist = re.findall('item_id": "(.*?)", "__item_image"', all_content)
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
clean_data.get_content3()
# clean_data.get_Ua()

#worker starting
