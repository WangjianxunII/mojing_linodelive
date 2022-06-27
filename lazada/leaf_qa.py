# coding=utf-8
import operator
from elasticsearch import Elasticsearch
import pymongo
from moojing import bearychat

es = 'http://10.19.12.67:9200'
ess = Elasticsearch(es)

#main/linodeprocess
db1 = pymongo.MongoClient('10.19.170.190').lazada

def get_last_qa_result(config_id):
    # 获取上一轮统计结果
    res = db1.leaf_qa_result.find({'config_id': config_id})
    if not res.count():
        return {}
    try:
        res = res.sort('ts', -1)[0]
        return res
    except:
        return {}


def get_leaf_data(index):
    bulk_num = 5000
    body = {"query": {"match_all": {}}}
    res = ess.search(index=index, body=body, scroll='5m', size=bulk_num, request_timeout=60)
    hits = res['hits']['hits']
    # print hits
    total = res['hits']['total']['value']
    # print total
    scroll_id = res['_scroll_id']
    f_num = total / bulk_num + 1
    leaf_spec_cat_count = {}
    for i in range(0, f_num):
        query_scroll = ess.scroll(scroll_id=scroll_id, scroll='5m', request_timeout=60)['hits']['hits']
        if i == 0:
            query_scroll += hits
        for q in query_scroll:
            item = q['_source']
            # print item
            # {u'original_price': 39.0, u'sku_id': u'1787510616', u'__cat6_name': u'', u'skus': [{u'id': u'610036274_SGAMZ-1787510616'}], u'__reviewcount': 1516, u'_field_00': u'get_list', u'__price': 26.9, u'__shop_id': u'100011442', u'sku': u'610036274_SGAMZ', u'ratings': 4.78957783641161, u'__brand_name': u'Logitech', u'__cat5_name': u'', u'__cat5_id': u'', u'__cat1_id': u'42062201', u'location': u'Singapore', u'__item_url': u'//www.lazada.sg/products/top-seller-logitech-mk215-wireless-keyboard-mouse-combo-small-footprint-ultra-compact-work-from-home-home-based-learning-i610036274-s1787510616.html?search=1&freeshipping=1&fastshipping=0&priceCompare=&sale=88&price=26.9&review=1516&ratingscore=4.78957783641161&location=Singapore&stock=1&lang=en', u'is_ad': 0, u'__sales': 2367.2, u'__cat6_id': u'', u'__ts': u'2022-04-29', u'__item_id': u'610036274', u'__item_image': u'https://sg-live-01.slatic.net/p/fb84587cf6be6e2d88a731877aad1803.jpg', u'plat': u'sg', u'discount': u'-31%', u'__item_name': u'(Top Seller) Logitech MK215 Wireless Keyboard & Mouse Combo (Small Footprint, Ultra Compact)  (Work From Home, Home Based Learning)', u'__sold': 88, u'__cat2_name': u'Computer Accessories', u'categories': [42062201, 78, 98, 10002910], u'__cat1_name': u'Electronics Accessories', u'__cat3_id': u'98', u'__cat3_name': u'Keyboards', u'__cat4_id': u'10002910', u'__brand_id': u'24954', u'__cat2_id': u'78', u'__shop_name': u'Logitech Official Store', u'__cat4_name': u'Mice & Keyboard Combos'}
            leaf_cid = item.get('categories')[-1]
            cat_name_key = '__cat%s_name' % (item.get('categories').index(leaf_cid) + 1)
            cat_name = item.get(cat_name_key)
            if not leaf_cid:
                break
            if leaf_spec_cat_count.get(leaf_cid):
                leaf_spec_cat_count[leaf_cid]['count'] += 1
            else:
                leaf_spec_cat_count[leaf_cid] = {'count': 1, 'sub_categroy_name': cat_name}
    return leaf_spec_cat_count


def get_leaf_diff(curr_raw_data, config_id):

    last_raw_data = get_last_qa_result(config_id)#获取上次数据
    leaf_count = {}
    for key in curr_raw_data.keys():
        leaf_count['%s'%key] = {}
        c_count = curr_raw_data[key].get('count')  # 这次
        l_count = last_raw_data.get('leaf_qa_result').get('%s'%key, {}).get('current_count')  # 上次
        if l_count:
            growth_count = c_count - l_count
            growth_rate = float(growth_count) / l_count
        else:
            growth_count = c_count
            growth_rate = 1
        leaf_count['%s'%key]['current_count'] = c_count
        leaf_count['%s'%key]['growth_count'] = growth_count
        leaf_count['%s'%key]['growth_rate'] = growth_rate
        leaf_count['%s'%key]['sub_categroy_name'] = curr_raw_data[key].get('sub_categroy_name')
    return leaf_count

def insert_qa_result(config_id, ts, result):

    # 将QA结果写到mongo
    insert_data = {'config_id': config_id, 'ts': ts, 'leaf_qa_result': result, 'leaf': 'true'}
    db1.leaf_qa_result.insert(insert_data)
    print 'insert success'

def gen_send_msg(raw_data, index):
    keys_list = raw_data.keys()

    negative_growth_items = []
    growth_items = []
    for k in keys_list:
        sub_item = raw_data.get(k)
        sub_item['sub_categroy_id'] = k
        if raw_data.get(k).get('growth_count') < 0:
            sub_item['growth_count'] = int(str(sub_item.get('growth_count')).replace('-', '').strip())
            negative_growth_items.append(sub_item)
        else:
            growth_items.append(sub_item)
    sorted_negative_growth_items = sorted(negative_growth_items, key=operator.itemgetter('growth_count'), reverse=True)
    sorted_growth_items = sorted(growth_items, key=operator.itemgetter('growth_count'), reverse=True)
    # print sorted_negative_growth_items

    # 构建发送通知内容
    msg = u'%sQA结果:\n' % index
    msg += u'所有叶子类目环比:\n'
    msg += u'增长叶子类目环比：\n'
    for k in sorted_growth_items:
        msg += u'类目id:%s\t类目名称:%s\t数量:%s\t环比:%.2f\t变化数量:%s\n' % (
            k['sub_categroy_id'], k['sub_categroy_name'], k['current_count'], k['growth_rate'],
            k['growth_count'])
    msg += u'减少叶子类目环比：\n'
    for k in sorted_negative_growth_items:
        msg += u'类目id:%s\t类目名称:%s\t数量:%s\t环比:%.2f\t变化数量:-%s\n' % (
            k['sub_categroy_id'], k['sub_categroy_name'], k['current_count'], k['growth_rate'],
            k['growth_count'])

    print msg

    seed_sms(msg)
def seed_sms(content):
    bearychat.send_webhook(content, 'wangjianxun')

if __name__ == '__main__':
    import sys
    current_config_id = sys.argv[1]
    current_config_units_list = current_config_id.split('_')
    c_config_id_l = current_config_units_list[:2]
    c_ts_l = current_config_units_list[2:]

    c_config_id = '_'.join(c_config_id_l)
    c_ts = '_'.join(c_ts_l)

    # curr_count = get_leaf_data('lazada_sg_2022_05_26')
    curr_count = get_leaf_data(current_config_id)
    # c_config_id = 'lazada_sg'
    # c_ts = '2022_05_26'
    res = get_leaf_diff(curr_count, c_config_id)#计算qa结果
    # print res
    insert_qa_result(c_config_id, c_ts, res)#qa结果存到mongo
    gen_send_msg(res, current_config_id)




