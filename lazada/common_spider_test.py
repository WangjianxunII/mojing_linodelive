#coding=utf-8
import json
import random
import re
import urllib

from moojing.spiderman.lazadasign import get_data_and_header
from moojing.spiderman.tbnewee import get_new_ee

seed = {"name" : "Men's Care", "plat" : "sg", "depth" : 2, "child_count" : 5, "category_url" : "//www.lazada.sg/shop-mens-care/", "path" : [ "965437", "1646" ], "id" : "1646" }
# 获取类目下商品列表
acm = seed['acm']
scm = seed['scm']
api = "mtop.lazada.gsearch.appsearch"
v = '1.0'
device_id = seed.get('device_id')
utd_id = seed.get('utd_id')
ee88 = seed.get('ee88')
ee112 = seed.get('ee112')
stid_umt = seed.get('stid_umt')
path = seed['path']
category_url = seed['category_url']
plat = seed['plat']
page = seed.get('page', 1)
reserve_price = seed.get('reserve_price')

if not device_id or not utd_id:
    print '开始获取EE'
    ee88, ee112, stid_umt, utdid, devid = get_new_ee()
    utd_id = utdid
    device_id = devid
ex_params = {'utdid': utd_id,
             "x_umt": stid_umt,
             'deviceId': device_id
             }
def build_search_data(acm, scm, category_url, page, device_id, utd_id, reserve_price=None):
    url_key = category_url.split("/")[3].split('?')[0]
    speed = random.random() * 20
    cat_pos = ''.join(re.findall('pos=(\d+)', category_url))
    sort = "order"  # order 销量 pricedesc 价格
    original_url = "http:" + category_url + '&from=lp_category&searchFlag=1'
    if "?" not in original_url:
        original_url = "http:" + category_url + '?from=lp_category&searchFlag=1'
    parma = {
        "__original_url__": urllib.quote(original_url),
        "acm": acm,
        "adjustID": "",
        "deviceID": device_id,
        "firstSearch": "true",
        "latitude": "0.0",
        "longitude": "0.0",
        "n": "10",
        "page": "%s" % page,
        "pos": cat_pos,
        "rainbow": "122,130,38,7,140",
        "scm": scm,
        "searchFlag": "1",
        "sort": sort,
        "from": "filter",
        "speed": "%s" % speed,
        "sversion": "5.0",
        "ttid": "1529386686433@lazada_android_6.75.1",
        "url_key": url_key + "/",
        "userID": "",
        "utd_id": utd_id,
        "vm": "nw"}
    if reserve_price:
        parma["price"] = "%s-%s" % (reserve_price[0], reserve_price[1])
    return parma

parmas = build_search_data(acm, scm, category_url, page, device_id, utd_id, reserve_price=reserve_price)
print 'parmas:', parmas
data, headers = get_data_and_header(api, json.dumps(parmas), v, extra_params=ex_params, ee88=ee88, ee112=ee112)
print 'data:', data
print 'headers:', headers
params = {
    "data": data['data'],
}
print params
# url = "https://acs-m.%s/gw/%s/%s/" % (DOMAIN[plat], api, v)
# print 'url:', url