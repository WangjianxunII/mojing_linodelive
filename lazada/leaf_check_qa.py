# coding=utf-8
from elasticsearch import Elasticsearch
import pymongo

es = 'http://10.19.12.67:9200'
ess = Elasticsearch(es)

# spec_cat = {u'10000380': {'count': 2340, 'leaf': False, 'level': 2}, u'10000656': {'count': 166, 'leaf': True, 'level': 3}, u'10000661': {'count': 169, 'leaf': True, 'level': 3}, u'10000678': {'count': 59, 'leaf': True, 'level': 3}, u'10000667': {'count': 97, 'leaf': True, 'level': 3}, u'10000666': {'count': 238, 'leaf': True, 'level': 3}, u'10000665': {'count': 172, 'leaf': True, 'level': 3}, u'10000664': {'count': 217, 'leaf': True, 'level': 3}, u'10000685': {'count': 93, 'leaf': True, 'level': 3}, u'10000684': {'count': 224, 'leaf': True, 'level': 3}, u'10000687': {'count': 353, 'leaf': True, 'level': 3}, u'10000668': {'count': 28, 'leaf': True, 'level': 3}, u'10000681': {'count': 204, 'leaf': True, 'level': 3}, u'10000698': {'count': 128, 'leaf': True, 'level': 3}, u'10000699': {'count': 61, 'leaf': True, 'level': 3}, u'10000682': {'count': 380, 'leaf': True, 'level': 3}, u'10000686': {'count': 79, 'leaf': True, 'level': 3}, u'10000660': {'count': 15, 'leaf': True, 'level': 3}, u'10000340': {'count': 13342, 'leaf': False, 'level': 1}, u'10000689': {'count': 56, 'leaf': True, 'level': 3}, u'10000657': {'count': 149, 'leaf': True, 'level': 3}, u'10000702': {'count': 45, 'leaf': True, 'level': 3}, u'10000653': {'count': 11, 'leaf': True, 'level': 3}, u'10000658': {'count': 155, 'leaf': True, 'level': 3}, u'10000650': {'count': 98, 'leaf': True, 'level': 3}, u'62090202': {'count': 1, 'leaf': True, 'level': 3}, u'10000677': {'count': 46, 'leaf': True, 'level': 3}, u'10000375': {'count': 752, 'leaf': False, 'level': 2}, u'10000673': {'count': 13, 'leaf': True, 'level': 3}, u'10000719': {'count': 943, 'leaf': True, 'level': 3}, u'10000679': {'count': 136, 'leaf': True, 'level': 3}, u'10000717': {'count': 140, 'leaf': True, 'level': 3}, u'10000716': {'count': 163, 'leaf': True, 'level': 3}, u'10000715': {'count': 110, 'leaf': True, 'level': 3}, u'10000714': {'count': 253, 'leaf': True, 'level': 3}, u'10000713': {'count': 1368, 'leaf': True, 'level': 3}, u'10000669': {'count': 221, 'leaf': True, 'level': 3}, u'10000711': {'count': 1, 'leaf': True, 'level': 3}, u'10000710': {'count': 73, 'leaf': True, 'level': 3}, u'10000670': {'count': 132, 'leaf': True, 'level': 3}, u'10000671': {'count': 413, 'leaf': True, 'level': 3}, u'10000654': {'count': 700, 'leaf': True, 'level': 3}, u'10000655': {'count': 39, 'leaf': True, 'level': 3}, u'10000379': {'count': 1133, 'leaf': False, 'level': 2}, u'10000378': {'count': 513, 'leaf': False, 'level': 2}, u'10000676': {'count': 105, 'leaf': True, 'level': 3}, u'10000651': {'count': 157, 'leaf': True, 'level': 3}, u'10000692': {'count': 663, 'leaf': True, 'level': 3}, u'10000374': {'count': 1444, 'leaf': False, 'level': 2}, u'10000377': {'count': 3895, 'leaf': False, 'level': 2}, u'10000376': {'count': 1287, 'leaf': False, 'level': 2}, u'10000696': {'count': 560, 'leaf': True, 'level': 3}, u'10000697': {'count': 46, 'leaf': True, 'level': 3}, u'10000694': {'count': 497, 'leaf': True, 'level': 3}, u'10000680': {'count': 116, 'leaf': True, 'level': 3}, u'10000674': {'count': 39, 'leaf': True, 'level': 3}, u'10000662': {'count': 12, 'leaf': True, 'level': 3}, u'10000373': {'count': 1978, 'leaf': False, 'level': 2}, u'10000659': {'count': 10, 'leaf': True, 'level': 3}, u'10000688': {'count': 82, 'leaf': True, 'level': 3}, u'10000683': {'count': 4, 'leaf': True, 'level': 3}, u'10000690': {'count': 241, 'leaf': True, 'level': 3}, u'42018803': {'count': 157, 'leaf': True, 'level': 3}, u'42018802': {'count': 14, 'leaf': True, 'level': 3}, u'10000693': {'count': 75, 'leaf': True, 'level': 3}, u'10000663': {'count': 29, 'leaf': True, 'level': 3}, u'10000708': {'count': 6, 'leaf': True, 'level': 3}, u'10000675': {'count': 2, 'leaf': True, 'level': 3}, u'10000712': {'count': 306, 'leaf': True, 'level': 3}, u'10000649': {'count': 424, 'leaf': True, 'level': 3}, u'10000648': {'count': 276, 'leaf': True, 'level': 3}, u'10000652': {'count': 69, 'leaf': True, 'level': 3}, u'10000709': {'count': 50, 'leaf': True, 'level': 3}, u'10000695': {'count': 4, 'leaf': True, 'level': 3}, u'10000672': {'count': 5, 'leaf': True, 'level': 3}, u'10000704': {'count': 264, 'leaf': True, 'level': 3}, u'10000705': {'count': 288, 'leaf': True, 'level': 3}, u'10000706': {'count': 373, 'leaf': True, 'level': 3}, u'10000707': {'count': 185, 'leaf': True, 'level': 3}, u'10000700': {'count': 4, 'leaf': True, 'level': 3}, u'10000701': {'count': 49, 'leaf': True, 'level': 3}, u'10000691': {'count': 126, 'leaf': True, 'level': 3}, u'10000703': {'count': 155, 'leaf': True, 'level': 3}}


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
            if not leaf_cid:
                break
            if leaf_spec_cat_count.get(leaf_cid):
                leaf_spec_cat_count[leaf_cid]['count'] += 1
            else:
                leaf_spec_cat_count[leaf_cid] = {'count': 1}
    return leaf_spec_cat_count



def get_leaf_diff(last, curr):
    all_count = {}
    leaf_count = {}
    for key in curr.keys():
        all_count[key] = {}
        leaf_count[key] = {} 
        c_count = curr[key].get('count')#这次
        l_count = last.get(key, {}).get('count')#上次
        if l_count:
            growth_count = c_count - l_count
            growth_rate = float(growth_count)/l_count
        else:
            growth_count = c_count
            growth_rate = 1
        all_count[key]['current_count'] = c_count
        all_count[key]['growth_count'] = growth_count
        all_count[key]['growth_rate'] = growth_rate
    return all_count



last_count = get_leaf_data('lazada_sg_2022_04_29')
curr_count = get_leaf_data('lazada_sg_2022_05_26')
# print curr_count
print get_leaf_diff(last_count, curr_count)





