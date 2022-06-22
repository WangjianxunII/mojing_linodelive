# coding:utf-8
import pandas as pd
from elasticsearch import Elasticsearch

es = 'http://10.19.12.67:9200'
ess = Elasticsearch(es)

indexs = ['lazada_ph_2022_05_28','lazada_th_2022_05_28','lazada_vn_2022_05_27','lazada_id_2022_05_26','lazada_my_2022_05_26','lazada_sg_2022_05_26']


# body={"query":{"match_all":{}}}
def get_sub(index):
    body = {"query": {"match_all": {}}}

    body1 = {
        "query": {
            'bool': {"must": [{"term": {
                u'__sold': 0
            }}
            ]}

        }
    }
    res = ess.search(index=index, body=body, scroll='5m', size=10000)
    hits = res['hits']['total']
    # print(hits)

    res1 = ess.search(index=index, body=body1, scroll='5m', size=10000)
    hits1 = res1['hits']['total']
    # print(hits1)
    print "有销量的数据：",index, (hits.get('value') - hits1.get('value'))
    print "没有销量的数据：",index, hits1.get('value')
    print "总商品数：",index, hits.get('value')
    print "*********"*5

def get_sub_item(index):
    pass

for i in indexs:
    get_sub(i)