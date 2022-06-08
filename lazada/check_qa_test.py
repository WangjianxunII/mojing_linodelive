# coding=utf-8
from elasticsearch import Elasticsearch

es = 'http://10.19.12.67:9200'
ess = Elasticsearch(es)

spec_cat = {u'10000380': {'count': 2340, 'leaf': False, 'level': 2}, u'10000656': {'count': 166, 'leaf': True, 'level': 3}, u'10000661': {'count': 169, 'leaf': True, 'level': 3}, u'10000678': {'count': 59, 'leaf': True, 'level': 3}, u'10000667': {'count': 97, 'leaf': True, 'level': 3}, u'10000666': {'count': 238, 'leaf': True, 'level': 3}, u'10000665': {'count': 172, 'leaf': True, 'level': 3}, u'10000664': {'count': 217, 'leaf': True, 'level': 3}, u'10000685': {'count': 93, 'leaf': True, 'level': 3}, u'10000684': {'count': 224, 'leaf': True, 'level': 3}, u'10000687': {'count': 353, 'leaf': True, 'level': 3}, u'10000668': {'count': 28, 'leaf': True, 'level': 3}, u'10000681': {'count': 204, 'leaf': True, 'level': 3}, u'10000698': {'count': 128, 'leaf': True, 'level': 3}, u'10000699': {'count': 61, 'leaf': True, 'level': 3}, u'10000682': {'count': 380, 'leaf': True, 'level': 3}, u'10000686': {'count': 79, 'leaf': True, 'level': 3}, u'10000660': {'count': 15, 'leaf': True, 'level': 3}, u'10000340': {'count': 13342, 'leaf': False, 'level': 1}, u'10000689': {'count': 56, 'leaf': True, 'level': 3}, u'10000657': {'count': 149, 'leaf': True, 'level': 3}, u'10000702': {'count': 45, 'leaf': True, 'level': 3}, u'10000653': {'count': 11, 'leaf': True, 'level': 3}, u'10000658': {'count': 155, 'leaf': True, 'level': 3}, u'10000650': {'count': 98, 'leaf': True, 'level': 3}, u'62090202': {'count': 1, 'leaf': True, 'level': 3}, u'10000677': {'count': 46, 'leaf': True, 'level': 3}, u'10000375': {'count': 752, 'leaf': False, 'level': 2}, u'10000673': {'count': 13, 'leaf': True, 'level': 3}, u'10000719': {'count': 943, 'leaf': True, 'level': 3}, u'10000679': {'count': 136, 'leaf': True, 'level': 3}, u'10000717': {'count': 140, 'leaf': True, 'level': 3}, u'10000716': {'count': 163, 'leaf': True, 'level': 3}, u'10000715': {'count': 110, 'leaf': True, 'level': 3}, u'10000714': {'count': 253, 'leaf': True, 'level': 3}, u'10000713': {'count': 1368, 'leaf': True, 'level': 3}, u'10000669': {'count': 221, 'leaf': True, 'level': 3}, u'10000711': {'count': 1, 'leaf': True, 'level': 3}, u'10000710': {'count': 73, 'leaf': True, 'level': 3}, u'10000670': {'count': 132, 'leaf': True, 'level': 3}, u'10000671': {'count': 413, 'leaf': True, 'level': 3}, u'10000654': {'count': 700, 'leaf': True, 'level': 3}, u'10000655': {'count': 39, 'leaf': True, 'level': 3}, u'10000379': {'count': 1133, 'leaf': False, 'level': 2}, u'10000378': {'count': 513, 'leaf': False, 'level': 2}, u'10000676': {'count': 105, 'leaf': True, 'level': 3}, u'10000651': {'count': 157, 'leaf': True, 'level': 3}, u'10000692': {'count': 663, 'leaf': True, 'level': 3}, u'10000374': {'count': 1444, 'leaf': False, 'level': 2}, u'10000377': {'count': 3895, 'leaf': False, 'level': 2}, u'10000376': {'count': 1287, 'leaf': False, 'level': 2}, u'10000696': {'count': 560, 'leaf': True, 'level': 3}, u'10000697': {'count': 46, 'leaf': True, 'level': 3}, u'10000694': {'count': 497, 'leaf': True, 'level': 3}, u'10000680': {'count': 116, 'leaf': True, 'level': 3}, u'10000674': {'count': 39, 'leaf': True, 'level': 3}, u'10000662': {'count': 12, 'leaf': True, 'level': 3}, u'10000373': {'count': 1978, 'leaf': False, 'level': 2}, u'10000659': {'count': 10, 'leaf': True, 'level': 3}, u'10000688': {'count': 82, 'leaf': True, 'level': 3}, u'10000683': {'count': 4, 'leaf': True, 'level': 3}, u'10000690': {'count': 241, 'leaf': True, 'level': 3}, u'42018803': {'count': 157, 'leaf': True, 'level': 3}, u'42018802': {'count': 14, 'leaf': True, 'level': 3}, u'10000693': {'count': 75, 'leaf': True, 'level': 3}, u'10000663': {'count': 29, 'leaf': True, 'level': 3}, u'10000708': {'count': 6, 'leaf': True, 'level': 3}, u'10000675': {'count': 2, 'leaf': True, 'level': 3}, u'10000712': {'count': 306, 'leaf': True, 'level': 3}, u'10000649': {'count': 424, 'leaf': True, 'level': 3}, u'10000648': {'count': 276, 'leaf': True, 'level': 3}, u'10000652': {'count': 69, 'leaf': True, 'level': 3}, u'10000709': {'count': 50, 'leaf': True, 'level': 3}, u'10000695': {'count': 4, 'leaf': True, 'level': 3}, u'10000672': {'count': 5, 'leaf': True, 'level': 3}, u'10000704': {'count': 264, 'leaf': True, 'level': 3}, u'10000705': {'count': 288, 'leaf': True, 'level': 3}, u'10000706': {'count': 373, 'leaf': True, 'level': 3}, u'10000707': {'count': 185, 'leaf': True, 'level': 3}, u'10000700': {'count': 4, 'leaf': True, 'level': 3}, u'10000701': {'count': 49, 'leaf': True, 'level': 3}, u'10000691': {'count': 126, 'leaf': True, 'level': 3}, u'10000703': {'count': 155, 'leaf': True, 'level': 3}}
def get_data(index, spec_cat):
    bulk_num = 5000
    body = {"query": {"match_all": {}}}
    res = ess.search(index=index, body=body, scroll='5m', size=bulk_num, request_timeout=60)
    print res
    hits = res['hits']['hits']
    total = res['hits']['total']['value']
    scroll_id = res['_scroll_id']
    f_num = total / bulk_num + 1
    spec_cat_count = {}
    for i in range(0, f_num):
        query_scroll = ess.scroll(scroll_id=scroll_id, scroll='5m', request_timeout=60)['hits']['hits']
        if i == 0:
            query_scroll += hits
        for q in query_scroll:
            item = q['_source']
            cat1_id = item.get('__cat1_id')
            if cat1_id in spec_cat:
                lenth = len(item.get('categories'))
                leaf = False
                for i in range(1, 7):
                    cid = item.get('__cat%s_id' % i)
                    if not cid:
                        break
                    if spec_cat_count.get(cid):
                        spec_cat_count[cid]['count'] += 1
                    else:
                        if i == lenth:
                            leaf = True
                        spec_cat_count[cid] = {'count': 1, 'level': i, 'leaf': leaf}
    return spec_cat_count


def get_diff(last, curr):
    all_count = {}
    leaf_count = {}
    for key in curr.keys():
        all_count[key]={}
        leaf_count[key] = {} 
        c_count = curr[key].get('count')
        is_leaf = curr[key].get('leaf')
        l_count = last.get(key, {}).get('count')
        if l_count:
            sub_count = c_count -l_count
            ring = float(sub_count)/l_count
        else:
            sub_count = c_count
            ring = 1
        all_count[key]['count'] = c_count
        all_count[key]['sub'] = sub_count
        all_count[key]['ring'] = ring
        if is_leaf:
            leaf_count[key]['count'] = c_count
            leaf_count[key]['sub'] = sub_count
            leaf_count[key]['ring'] = ring
    return all_count, leaf_count
            


# spec_cat_list = ['10000340', '10100758', '1819', '10100412', '9067', '10282', '10100083', '10000335', '42062201',
#                  '10000337', '10000336', '8706']
spec_cat_list = ['10000340']
last_count = get_data('lazada_sg_2022_04_29', spec_cat_list)
curr_count = get_data('lazada_sg_2022_05_26', spec_cat_list)
print curr_count
# print get_diff(last_count, curr_count)
# {u'10000380': {'count': 2340, 'leaf': False, 'level': 2}, u'10000656': {'count': 166, 'leaf': True, 'level': 3}, u'10000661': {'count': 169, 'leaf': True, 'level': 3}, u'10000678': {'count': 59, 'leaf': True, 'level': 3}, u'10000667': {'count': 97, 'leaf': True, 'level': 3}, u'10000666': {'count': 238, 'leaf': True, 'level': 3}, u'10000665': {'count': 172, 'leaf': True, 'level': 3}, u'10000664': {'count': 217, 'leaf': True, 'level': 3}, u'10000685': {'count': 93, 'leaf': True, 'level': 3}, u'10000684': {'count': 224, 'leaf': True, 'level': 3}, u'10000687': {'count': 353, 'leaf': True, 'level': 3}, u'10000668': {'count': 28, 'leaf': True, 'level': 3}, u'10000681': {'count': 204, 'leaf': True, 'level': 3}, u'10000698': {'count': 128, 'leaf': True, 'level': 3}, u'10000699': {'count': 61, 'leaf': True, 'level': 3}, u'10000682': {'count': 380, 'leaf': True, 'level': 3}, u'10000686': {'count': 79, 'leaf': True, 'level': 3}, u'10000660': {'count': 15, 'leaf': True, 'level': 3}, u'10000340': {'count': 13342, 'leaf': False, 'level': 1}, u'10000689': {'count': 56, 'leaf': True, 'level': 3}, u'10000657': {'count': 149, 'leaf': True, 'level': 3}, u'10000702': {'count': 45, 'leaf': True, 'level': 3}, u'10000653': {'count': 11, 'leaf': True, 'level': 3}, u'10000658': {'count': 155, 'leaf': True, 'level': 3}, u'10000650': {'count': 98, 'leaf': True, 'level': 3}, u'62090202': {'count': 1, 'leaf': True, 'level': 3}, u'10000677': {'count': 46, 'leaf': True, 'level': 3}, u'10000375': {'count': 752, 'leaf': False, 'level': 2}, u'10000673': {'count': 13, 'leaf': True, 'level': 3}, u'10000719': {'count': 943, 'leaf': True, 'level': 3}, u'10000679': {'count': 136, 'leaf': True, 'level': 3}, u'10000717': {'count': 140, 'leaf': True, 'level': 3}, u'10000716': {'count': 163, 'leaf': True, 'level': 3}, u'10000715': {'count': 110, 'leaf': True, 'level': 3}, u'10000714': {'count': 253, 'leaf': True, 'level': 3}, u'10000713': {'count': 1368, 'leaf': True, 'level': 3}, u'10000669': {'count': 221, 'leaf': True, 'level': 3}, u'10000711': {'count': 1, 'leaf': True, 'level': 3}, u'10000710': {'count': 73, 'leaf': True, 'level': 3}, u'10000670': {'count': 132, 'leaf': True, 'level': 3}, u'10000671': {'count': 413, 'leaf': True, 'level': 3}, u'10000654': {'count': 700, 'leaf': True, 'level': 3}, u'10000655': {'count': 39, 'leaf': True, 'level': 3}, u'10000379': {'count': 1133, 'leaf': False, 'level': 2}, u'10000378': {'count': 513, 'leaf': False, 'level': 2}, u'10000676': {'count': 105, 'leaf': True, 'level': 3}, u'10000651': {'count': 157, 'leaf': True, 'level': 3}, u'10000692': {'count': 663, 'leaf': True, 'level': 3}, u'10000374': {'count': 1444, 'leaf': False, 'level': 2}, u'10000377': {'count': 3895, 'leaf': False, 'level': 2}, u'10000376': {'count': 1287, 'leaf': False, 'level': 2}, u'10000696': {'count': 560, 'leaf': True, 'level': 3}, u'10000697': {'count': 46, 'leaf': True, 'level': 3}, u'10000694': {'count': 497, 'leaf': True, 'level': 3}, u'10000680': {'count': 116, 'leaf': True, 'level': 3}, u'10000674': {'count': 39, 'leaf': True, 'level': 3}, u'10000662': {'count': 12, 'leaf': True, 'level': 3}, u'10000373': {'count': 1978, 'leaf': False, 'level': 2}, u'10000659': {'count': 10, 'leaf': True, 'level': 3}, u'10000688': {'count': 82, 'leaf': True, 'level': 3}, u'10000683': {'count': 4, 'leaf': True, 'level': 3}, u'10000690': {'count': 241, 'leaf': True, 'level': 3}, u'42018803': {'count': 157, 'leaf': True, 'level': 3}, u'42018802': {'count': 14, 'leaf': True, 'level': 3}, u'10000693': {'count': 75, 'leaf': True, 'level': 3}, u'10000663': {'count': 29, 'leaf': True, 'level': 3}, u'10000708': {'count': 6, 'leaf': True, 'level': 3}, u'10000675': {'count': 2, 'leaf': True, 'level': 3}, u'10000712': {'count': 306, 'leaf': True, 'level': 3}, u'10000649': {'count': 424, 'leaf': True, 'level': 3}, u'10000648': {'count': 276, 'leaf': True, 'level': 3}, u'10000652': {'count': 69, 'leaf': True, 'level': 3}, u'10000709': {'count': 50, 'leaf': True, 'level': 3}, u'10000695': {'count': 4, 'leaf': True, 'level': 3}, u'10000672': {'count': 5, 'leaf': True, 'level': 3}, u'10000704': {'count': 264, 'leaf': True, 'level': 3}, u'10000705': {'count': 288, 'leaf': True, 'level': 3}, u'10000706': {'count': 373, 'leaf': True, 'level': 3}, u'10000707': {'count': 185, 'leaf': True, 'level': 3}, u'10000700': {'count': 4, 'leaf': True, 'level': 3}, u'10000701': {'count': 49, 'leaf': True, 'level': 3}, u'10000691': {'count': 126, 'leaf': True, 'level': 3}, u'10000703': {'count': 155, 'leaf': True, 'level': 3}}
