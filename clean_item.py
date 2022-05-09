# coding:utf-8
import re
class CLEAN_DATA:
    def __init__(self):
        self.data_list = []

    def get_content(self):
        with open('wangtest.txt','r') as f:
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

clean_data = CLEAN_DATA()
clean_data.get_content()
