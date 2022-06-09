# import pandas as pd
from elasticsearch import Elasticsearch

es = 'http://10.19.12.67:9200'
ess = Elasticsearch(es)
index = 'lazada_id_2022_05_26'
body = {"query": {"match_all": {}}}
# body={
#     "query":{
#         'bool':{"must":[{ "term": {
#          u'__cat1_id': u'275',
#         }},
#          { "term": {
#          u'__sold' : 0
#         }}
#                        ]}

#     }
# }
res = ess.search(index=index, body=body, scroll='5m', size=10000)
hits = res['hits']['total']
print hits
# wf =open('/share/home/maweiwei/wmatool/lazada/lazada_sg_4.txt','w')
# for m in res['hits']['hits']:
#     x = m['_source']
#     sold = x['__sold']
#     if int(sold) ==0:
#         continue
#     data = x['__item_id']
#     wf.write(data +'\n')

# wf.close()