#coding=utf-8
import datetime
import json
import urllib
import random
import pymongo
import re
import hashlib
import redis
from moojing import INFO, ERR
from moojing.spiderman.lazadasign import get_data_and_header
from moojing.spiderman.tbnewee import get_new_ee
from moojing.spiderman import jobqueue
from moojing.spiderman import BasicWorker
red = jobqueue.red
# red = redis.Redis(host='192.168.193.8', password='redixxxx', port=6380, db=10)


def get_md5(val):
    """把目标数据进行哈希，用哈希值去重更快"""
    md5 = hashlib.md5()
    md5.update(val.encode('utf-8'))
    return md5.hexdigest()

def red_add_item_id(data,plat):
    res = red.sadd('Lazada_set_%s'%plat, get_md5(data))  # 注意是 保存set的方式
    if res == 0:  # 若返回0,说明插入不成功，表示有重复
        return False
    else:
        return True

DOMAIN = {'my': 'lazada.com.my',  # 马来西亚
          'id': 'lazada.co.id',  # 印度尼西亚
          'vn': 'lazada.vn',  # 越南
          'th': 'lazada.co.th',  # 泰国
          'sg': 'lazada.sg',  # 新加坡
          'ph': 'lazada.com.ph',  # 菲律宾
          }
PRICE_RG = {
    'my': 0.01,  # 马来西亚 doller
    'id': 1,  # 印度尼西亚 rupiah
    'vn': 0.01,  # 越南 dong
    'th': 0.1,  # 泰国
    'sg': 0.01,  # 新加坡
    'ph': 0.1,  # 菲律宾
}

BACK_CAT = {}


def generate_deviceId():
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') for i in range(44))


def generate_utd_id():
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') for i in range(24))


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


def check_price_range(reserve_price):
    p1, p2 = reserve_price
    if p1 and p2:
        if float(p1) > float(p2):
            return False
    return True


def find_price_range(itemList, reserve_price, key='price', default_key='originalPrice', rg=0.1):
    if reserve_price is not None:
        p1, p2 = reserve_price
    else:
        p1, p2 = '', ''
    if p1 and p2:
        p1 = float(p1)
        p2 = float(p2)
        if p2 - p1 <= rg:
            return None
    price_max, price_min = 0, 999999999
    for item in itemList:
        #         INFO(item)
        price = float(item.get(key, 0))
        if price < price_min:
            if p1 and price < p1:
                continue
            price_min = price
        if price > price_max:
            if p2 and price > p2:
                continue
            price_max = price

    max_price = 999999999 if p2 == '' else float(p2)
    price_max = max_price

    min_price = 0 if p1 == '' else float(p1)
    price_min = min(price_min, min_price)

    if round(price_max - price_min, 2) <= rg:
        return None
    return round((price_max + price_min) / 2, 2)


def parse_data(data, reserve_price, path, plat, currentPage=1):
    res_list = data.get('data').get("mods").get('listItems', [])
    #     global BACK_CAT
    has_next = True
    bsplit = False
    mid_price = ''
    total_count = data.get('data').get("mainInfo").get("totalResults")
    items = []
    # INFO('path:%s, reserve_price:%s,page:%s,total_count:%s' % (path, reserve_price, currentPage, total_count))
    sold_count = 0
    for res in res_list:
        item = {}
        #         item['reserve_price'] = reserve_price
        #         item['total_count'] = total_count
        #         item['path'] =path
        item['plat'] = plat
        categories = res.get('categories')
        item['categories'] = categories
        for i in range(len(categories)):
            id_key = '__cat%s_id' % (i + 1)
            name_key = '__cat%s_name' % (i + 1)
            item[id_key] = categories[i]
            search_key = '%s-%s' % (plat, categories[i])
            item[name_key] = BACK_CAT.get(search_key, '')

        item['__item_name'] = res.get('name')
        item['__item_id'] = res.get('itemId')
        if not item['__item_id']:
            INFO("Invalid DATA")
            continue
        item['__item_image'] = res.get('image')
        item['__brand_id'] = res.get('brandId')
        item['__brand_name'] = res.get('brandName')
        item['ratings'] = res.get('ratingScore')
        item['__price'] = res.get('price')
        item['__item_url'] = res.get('productUrl')
        item['__reviewcount'] = res.get('review')
        item['__shop_name'] = res.get('sellerName')
        item['__shop_id'] = res.get('sellerId')
        item['skus'] = res.get('skus')
        item['original_price'] = res.get('originalPrice')
        item['discount'] = res.get('discount')
        item['location'] = res.get('location')
        item['sku'] = res.get("sku")
        item['sku_id'] = res.get('skuId')
        item['is_ad'] = res.get("isAD")
        item['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            item['__sold'] = res.get("itemSoldCntShow", '').replace("Sold/Month", '').replace(",", '').strip()
            sold_count += int(item['__sold'])
        except:
            continue
        if int(item.get('__sold')) > 0:
            red_status = red_add_item_id(item['__item_id'],plat)
            if red_status:
                detail_units(item)
            else:
                pass
        items.append(item)
    if sold_count == 0:
        INFO("PATH:%s, PRICE_RANG:%s,PAGE:%s, has no sold" % (path, reserve_price,currentPage))
        has_next = False
    else:
        has_next = True

    if total_count is None:
        return False, False, items, mid_price, 0
    elif int(total_count) == 0:
        return False, False, items, mid_price, 0
    total_count = int(total_count)
    if total_count > 102 * 10 and has_next:
        # 最大翻102页，每页10条
        price_rg = PRICE_RG[plat]
        mid_price = find_price_range(res_list, reserve_price, rg=price_rg)
        if mid_price:
            bsplit = True
            has_next = False
    if total_count <= currentPage * 10 or len(res_list) < 10:
        has_next = False

    return bsplit, has_next, items, mid_price, total_count

def detail_units(item):
    detail_jq.enqueue(json.dumps({
        'type': 'get_detail',
        'categories': item['categories'],
        '__item_url': item['__item_url'],
        'location': item['location'],
        '__item_id': item['__item_id'],
        '__sold': item['__sold'],
        'plat': item['plat'],
    }))
def get_item_list(ps, seed, app):
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
    # ee88 = ps.context.get("ee88")
    # ee112 = ps.context.get("ee112")
    # utdid = ps.context.get("utdid", "VL4YFxORE1l8vNdSXyqLwuNU")
    # stid_umt = ps.context.get("stid_umt", "UKEAya1LPCFpsAJ8y8b3EJdHUKEUKKFX")
    # devid = ps.context.get('devid', 'AzE3E0lHcH7vDnohICi-sfMFs9y9yzuuKeCvsOseXjmT')
    # if ps.context.get("ee_count") is None:
    #     ps.context['ee_count'] = 0
    # else:
    #     ps.context['ee_count'] = ps.context['ee_count'] + 1
    # if ps.context['ee_count'] % 100 == 0:
    #     try:
    #         ee88, ee112, stid_umt, utdid, devid = get_new_ee()
    #         ps.context['ee88'] = ee88
    #         ps.context['ee112'] = ee112
    #         ps.context['stid_umt'] = stid_umt
    #         ps.context['utdid'] = utdid
    #         ps.context['devid'] = devid
    #     except:
    #         ps.context['ee_count'] = ps.context['ee_count'] + 50
    #wjx
    if not device_id or not utd_id:
        INFO('开始获取EE')
        ee88, ee112, stid_umt, utdid, devid = get_new_ee()
        utd_id = utdid
        device_id = devid
    ex_params = {'utdid': utd_id,
                 "x_umt": stid_umt,
                 'deviceId': device_id
                 }
    parmas = build_search_data(acm, scm, category_url, page, device_id, utd_id, reserve_price=reserve_price)
    print 'parmas:',parmas
    data, headers = get_data_and_header(api, json.dumps(parmas), v, extra_params=ex_params, ee88=ee88, ee112=ee112)
    print 'data:',data
    print 'headers:',headers
    ps.headers = headers
    params = {
        "data": data['data'],
    }
    url = "https://acs-m.%s/gw/%s/%s/" % (DOMAIN[plat], api, v)
    print 'url:',url
    url += "?" + urllib.urlencode(params)
    return
    _r = ps.get_page(url)

    if not _r:
        try:
            if _r.status_code == 419:
                raise Exception, 'ITEM419 flood'
        except Exception,e:
            if 'ITEM419' in str(e):
                raise Exception, 'ITEM419 flood'
        raise Exception, 'net_work'
    res = json.loads(_r.text)
    if not res.get('data') or not res.get('data').get("mods") or not res.get('data').get("mainInfo"):
        raise Exception, 'flood'
    need_price_split, next_page, items, content, total_count = parse_data(res, reserve_price, path, plat,
                                                                          currentPage=page)

    if seed.get('pre_items'):
        dup_items = list(set(seed['pre_items']) & set([x['__item_id'] for x in items]))
        if len(dup_items) > 3:
            ERR('dupitems', seed, dup_items, seed['pre_items'], [x['__item_id'] for x in items])
            seed['retry'] = 0
            raise Exception('dupitems')
    if need_price_split:
        mid_price = content
        if reserve_price is None:
            reserve_price = ['', '']
        front = [reserve_price[0], str(mid_price)]
        price_rg = PRICE_RG[plat]
        back = [str(mid_price + price_rg), reserve_price[1]]
        if check_price_range(front):
            ee_88, ee_112, stid_umt, utdid, devid = get_new_ee()
            seed2 = seed.copy()
            seed2['page'] = 1
            seed2['device_id'] = devid
            seed2['utd_id'] = utdid
            seed2['ee88'] = ee_88
            seed2['ee112'] = ee_112
            seed2['stid_umt'] = stid_umt
            seed2['reserve_price'] = front
            seed2['retry'] = 0
            app.jq.enqueue(seed2)
        if check_price_range(back):
            seed2 = seed.copy()
            seed2['page'] = 1
            seed2['device_id'] = device_id
            seed2['utd_id'] = utd_id
            seed2['ee88'] = ee88
            seed2['ee112'] = ee112
            seed2['stid_umt'] = stid_umt
            seed2['reserve_price'] = back
            seed2['retry'] = 0
            app.jq.enqueue(seed2)

    if next_page and total_count:
        real_total_count = seed.get('real_total_count', total_count)
        max_page = min([int(real_total_count / 10) + 1, 102])
        thisitems = [x['__item_id'] for x in items]
        if page <= max_page:
            seed2 = seed.copy()
            seed2.pop('retry', None)
            seed2['page'] = int(page) + 1
            seed2['real_total_count'] = real_total_count
            seed['pre_items'] = thisitems
            app.jq.enqueue(json.dumps(seed2))

    for item in items:
        item['page'] = page
        item['plat'] = plat
    return items

def common_run(jq):
    plat = 'sg'
    detail_project = 'lazada_detail_%s_'%plat
    detail_jq = jobqueue.Queue('{0}'.format(detail_project))
    global detail_jq
    # 读取类目数据爬取列表
    db = pymongo.MongoClient('192.168.198.173').lazada
    back_cats = db.back_cats.find({'plat': plat})
    for i in back_cats:
        key = '%s-%s' % (i.get('plat'), i.get('category_id'))
        BACK_CAT[key] = i.get('name')
    if jq.part_id == 1:
        jq.reset()
        detail_jq.reset()
        duplicate_removal_key = 'Lazada_set_%s' % plat
        red.delete(duplicate_removal_key)

        # import subprocess
        # # subprocess.check_output(
        # subprocess.Popen(
        #     'ssh lishopper1 "cd /share/home/wangjianxun/mojing_spiderman/linode/crawler_util/lazada/detail_shell_units; ./ssh_lishopper2506.sh {}"'.format(plat),
        #     shell=True
        # )

        for cat in db.cats.find({'plat': plat}):
            if cat.get('plat') != plat:
                continue
            if not cat.get("category_url") or 'www.lazada' not in cat.get("category_url"):
                continue
            if cat.get('depth') == 2 and cat.get('child_count') != 0:
                continue
            jq.enqueue({'type': 'get_item_list',
                        'scm': cat.get("scm", ''),
                        'acm': cat.get("acm", ''),
                        'category_id': cat.get('id'),
                        'path': cat.get('path'),
                        'plat': cat.get('plat'),
                        # 'device_id': generate_deviceId(),
                        # 'utd_id': generate_utd_id(),
                        'category_url': cat.get("category_url")
                        })

if __name__ == '__main__':
    worker = BasicWorker(project='common_run', proxy_type='rproxy', user_agent_type='mobile', sleep_time=5, worker_retry=50)
    worker.run()