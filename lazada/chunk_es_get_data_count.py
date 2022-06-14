# import pandas as pd
from elasticsearch import Elasticsearch

es = 'http://10.19.12.67:9200'
ess = Elasticsearch(es)
index = 'lazada_my_2022_05_26'
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
#{"item_id": "2886218318", "item_url": "//www.lazada.co.id/products/12pcs-diamond-plus-white-vit-e-tutup-biru-i2886218318-s11631334854.html?search=1&fastshipping=0&priceCompare=skuId%3A11631334854%3Bsource%3Alazada-search-28551%3Bsn%3Aca15c693afa8e8d7214992ab7755c7bd%3BoriginPrice%3A3750000%3BvoucherPrice%3A3750000%3Btimestamp%3A1649468360449&sale=8&price=37500.00&review=64&ratingscore=4.890625&location=&stock=1&lang=en", "__sold": 8, "categories": [3509, 3511, 3512, 6234], "location": null}
