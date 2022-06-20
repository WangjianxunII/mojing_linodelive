# coding:utf-8
import json
import random
import re
import time
from elasticsearch import Elasticsearch

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
    def get_list_content4(self):

        sold_count_lsit = []
        # with open('wangtest.txt','r') as f:
        for p in range(1,10):
            try:
                with open('/data/lazada_ph/lazada_ph__2022_05_28_%s_rproxy.txt'%p, 'r') as f:
                # with open('./%s.txt'%p, 'r') as f:
                    for line in f:
                        sold_count_l = re.findall('__sold": "(.*?)", "', line)
                        item_id_l = re.findall('__item_id": "(.*?)", "', line)
                        # print 'item_id:', item_id_l
                        item = {}
                        if item_id_l:
                            if item_id_l[0]:
                                item['item_id'] = item_id_l[0]
                            else:
                                item['item_id'] = ''
                        else:
                            print line
                            item['item_id'] = ''
                            # break
                        if sold_count_l:
                            if sold_count_l[0]:
                                item['sold_count'] = sold_count_l[0]
                            else:
                                item['sold_count'] = ''
                        else:
                            item['sold_count'] = ''
                        if item['item_id'] not in sold_count_lsit and item['sold_count']:
                            sold_count_lsit.append(item['item_id'])

                # print "有销量的数据：", len(sold_count_lsit)

            except:
                pass
        print "有销量的数据：", len(sold_count_lsit)

    def get_test(self):
        sold_count_lsit = []
        with open('/data/lazada_ph/lazada_ph__2022_05_28_%s_rproxy.txt' % 1, 'r') as f:
            # with open('./%s.txt'%p, 'r') as f:
            for line in f:
                sold_count_l = re.findall('__sold": "(.*?)", "', line)
                item_id_l = re.findall('__item_id": "(.*?)", "', line)
                # print 'item_id:', item_id_l
                item = {}
                if item_id_l:
                    if item_id_l[0]:
                        item['item_id'] = item_id_l[0]
                    else:
                        item['item_id'] = ''
                else:
                    print line
                    item['item_id'] = ''
                    break
                if sold_count_l:
                    if sold_count_l[0]:
                        item['sold_count'] = sold_count_l[0]
                    else:
                        item['sold_count'] = ''
                else:
                    item['sold_count'] = ''
                if item['item_id'] not in sold_count_lsit and item['sold_count']:
                    sold_count_lsit.append(item['item_id'])

        print "有销量的数据：", len(sold_count_lsit)

    def get_test_2(self):
        es = 'http://10.19.12.67:9200'
        ess = Elasticsearch(es)
        item_list = []
        index = 'lazada_sg_2022_05_26'
        # 根据索引获取es中的数据
        bulk_num = 5000
        body = {"query": {"match_all": {}}}
        res = ess.search(index=index, body=body, scroll='5m', size=bulk_num, request_timeout=60)
        hits = res['hits']['hits']
        total = res['hits']['total']['value']
        scroll_id = res['_scroll_id']
        f_num = total / bulk_num + 1
        sold_count = 0
        for i in range(0, f_num):
            query_scroll = ess.scroll(scroll_id=scroll_id, scroll='5m', request_timeout=60)['hits']['hits']
            if i == 0:
                query_scroll += hits

            for q in query_scroll:
                if q.get('__sold') > 0:
                    if q.get('__item_id') not in item_list:
                        sold_count += 1
        print "有销量的数据：", sold_count
        print "有销量的数据itemlist：", len(item_list)
    def get_content5(self):
        with open('/data/lazada_detail/lazada_detail_sg_2022_06_13_1_rproxy.txt') as f:
        # with open('./test_') as f:
            d_count = 0
            sold_count = 0
            no_sold_count = 0
            for line in f:
                d_count += 1
                datalist = re.findall('__sold": "(.*?)", "guideApp":', line)
                # print datalist
                for i in datalist:
                    if i:
                        sold_count += 1
                    else:
                        no_sold_count += 1
            print "有销量的数据：", sold_count
            print "没有销量的数据：", no_sold_count
            print "总商品数：", d_count
clean_data = CLEAN_DATA()
# clean_data.get_content()
# clean_data.get_content2()
# clean_data.get_content3()
# clean_data.get_list_content4()
# clean_data.get_test()
clean_data.get_test_2()
# clean_data.get_content5()
# clean_data.get_Ua()

#worker starting
