# coding=utf-8
from elasticsearch import Elasticsearch

es = 'http://10.19.12.67:9200'
ess = Elasticsearch(es)


def get_data(index, spec_cat):
    bulk_num = 5000
    body = {"query": {"match_all": {}}}
    res = ess.search(index=index, body=body, scroll='5m', size=bulk_num, request_timeout=60)
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
            leaf_count[key]['ring']  = ring
    return all_count, leaf_count
            


spec_cat_list = ['10000340', '10100758', '1819', '10100412', '9067', '10282', '10100083', '10000335', '42062201',
                 '10000337', '10000336', '8706']
last_count = get_data('lazada_sg_2022_04_29', spec_cat_list)
curr_count = get_data('lazada_sg_2022_05_26', spec_cat_list)

print get_diff(last_count, curr_count)
