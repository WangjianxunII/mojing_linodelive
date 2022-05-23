# coding:utf-8
import re
import time


class CLEAN_DATA:
    def __init__(self):
        self.data_list = []

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
        with open('content213.txt', 'r') as f:
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
        with open('/data/test/catappitems_taobao_test5_2022_05_19_24_rproxy.txt', 'r') as f:
            all_content_list = f.readlines()
            # datalist = re.findall(',item_id:(.*?),price', all_content)
            # d_count = len(datalist)
            for i in all_content_list:

                # i = 'cat_items{"comment": "", "loc": "", "clickTrace": "query:%E8%BF%9E%E8%A1%A3%E8%A3%99;nid:673438202146;cat_id:50010850;seller_id:4002489870;seller_type:1;src:mainse;recType:;rn:abf9760f0c7b5ae4cd66c7d9ff19dc17;c_flag:false;client:android;sp_rank_features:;wlsort:0;price:89;sold:6519;sort:_sale;tpp_bucket:1;catepgoryp:50010850 16 0;sumtips:bsl_165", "uid": "4002489870", "title": "\u68ee\u9a6c\u8fde\u8863\u88d9v\u9886\u6ce1\u6ce1\u8d28\u611f\u683c\u7eb9\u751c\u7f8e", "price_type": "price", "price": "339.00", "pic": "http://g.search2.alicdn.com/img/bao/uploaded/i4/i1/4002489870/O1CN01QCI9uU2MmVvDaSFON_!!0-item_pic.jpg", "buy_count": 6519, "ww": "", "brand_id": null, "shop_type": "tmall", "cid": "", "crawl_time": "2022-05-19 09:27:46", "seed": {"q": "\u8fde\u8863\u88d9", "type": "cat_items", "pageno": 1}, "item_id": "673438202146", "pro_price": "89.90", "is_global": false, "back_cid": "", "sold": 6519, "iconList": ["tmall", "baoyounew"]}\n'
                i = i.replace('cat_items','').replace('\n','').strip()
                print eval(i).get('item_id')
                time.sleep(2)
            #     if i not in self.data_list:
            #         self.data_list.append(i)
            #     else:
            #         print i
            #         # print self.data_list
            # print "去重前 抓取数据：", d_count
            # print "去重后 抓取数据：",len(self.data_list)

clean_data = CLEAN_DATA()
# clean_data.get_content()
# clean_data.get_content2()
clean_data.get_content3()

#worker starting
