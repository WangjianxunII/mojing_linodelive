# coding=utf-8

try:
    import sockinfo
except:
    pass
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import datetime
import re
import json
import urllib
from hashlib import md5
import time
from collections import OrderedDict
from moojing import openlog, INFO, ERR, DBG
from moojing.spiderman import BasicWorker
from qa_field_type import field_type_qa
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()

"""
用于请求淘宝H5 搜索类目爬虫
pm:http://pm.moojing.com/issues/50801
需要先获取cna,然后抓取数据
"""

locs = ["广州", "深圳", "杭州", "福州", "苏州", "南京", "安徽", "澳门", "福建", "甘肃", "广东", "广西", "贵州", "海南", "河北", "河南", "湖北", "湖南",
        "黑龙江", "江苏", "吉林", "辽宁", "内蒙古", "宁夏", "青海", "山东", "山西", "陕西", "四川", "台湾", "西藏", "新疆", "香港", "云南", "浙江", "北京",
        "上海", "天津", "重庆", "海外"]


def find_price_range(min_price, max_price, itemList, reserve_price, key='priceWithRate', default_key='price', rg=0.05):
    # return None
    if reserve_price is not None:
        p1, p2 = reserve_price
    else:
        p1, p2 = '', ''
    if p1 and p2:
        p1 = float(p1)
        p2 = float(p2)
        if round(p2 - p1, 2) <= rg:
            return None
    price_max, price_min = 0, 999999999
    for item in itemList:
        default_key_ = default_key if item.get(default_key) else "sku_discnt_price"
        price = float(str(item.get(key, item[default_key_])).split('\x03')[0])
        if price < price_min:
            if p1 and price < p1:
                continue
            price_min = price
        if price > price_max:
            if p2 and price > p2:
                continue
            price_max = price

    if p2 != '':
        max_price = float(p2)
    price_max = max_price

    if p1 != '':
        min_price = float(p1)
    price_min = min(price_min, min_price)

    if round(price_max - price_min, 2) <= rg:
        return None

    # print price_max, price_min, round((price_max+price_min)/2, 2)
    return round((price_max + price_min) / 2, 2)


def check_price_range(reserve_price):
    p1, p2 = reserve_price
    if p1 and p2:
        if float(p1) > float(p2):
            return False
    return True


def get_sign(token, timestamp, data):
    """
    淘宝h5接口签名sign计算
    :param timestamp: 13位时间戳
    :param data: 接口发送的参数 data str
    """
    text = '{}&{}&12574478&{}'.format(token, timestamp, data)
    result = str(md5(text).hexdigest())
    return result


def get_api_resp(data, ps):
    """
    封装的请求 mtop.relationrecommend.WirelessRecommend.recommend, data 有两种格式
    """
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'sec-ch-ua-mobile': '?0',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39',
        'sec-ch-ua-platform': '"Windows"',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'script',
        'Referer': 'https://main.m.taobao.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    ps.headers.update(headers)
    cookies = ps.session.cookies.get_dict()
    token = cookies.get("_m_h5_tk")
    token = "" if token is None else token.split("_")[0].strip()
    timestamp = int(time.time() * 1000)
    post_data = OrderedDict()
    post_data["jsv"] = "2.6.2"
    post_data["appKey"] = "12574478"
    post_data["t"] = str(timestamp)
    post_data["sign"] = get_sign(token, timestamp, data)
    post_data["api"] = "mtop.relationrecommend.WirelessRecommend.recommend"
    post_data["v"] = "2.0"
    post_data["type"] = "jsonp"
    post_data["dataType"] = "jsonp"
    post_data["callback"] = "mtopjsonp2"
    post_data["data"] = data
    url = "https://h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/?" + urllib.urlencode(
        post_data)
    resp = ps.session.get(url, headers=ps.headers, proxies=ps.proxies, verify=False, cookies=cookies, timeout=10)
    return ps.guess_result(resp)


def get_cna(ps):
    """
    获取cna cookie
    """
    headers = {
        'authority': 'log.mmstat.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'accept': '*/*',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-dest': 'script',
        'referer': 'https://main.m.taobao.com/',
        'accept-language': 'zh-CN,zh;q=0.9',
    }
    for i in range(10):
        url = "https://log.mmstat.com/eg.js?t={}".format(int(time.time() * 1000))
        ps.session.get(url, headers=headers, proxies=ps.proxies, timeout=10)
        if "cna" in ps.session.cookies.get_dict():
            INFO("gen cna finished")
            break
    else:
        raise Exception("get_cna_failed")


def get_cookie2(ps):
    headers = {
        'authority': 'login.m.taobao.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'zh-CN,zh;q=0.9',
    }
    for i in range(10):
        url = "https://login.m.taobao.com/login.htm"
        ps.session.get(url, headers=headers, proxies=ps.proxies, timeout=10)
        if "cookie2" in ps.session.cookies.get_dict():
            INFO("gen cookie2 finished")
            break
    else:
        raise Exception("get_cookie2_failed")


def gen_cookie(ps):
    """
    获取cookie,cna 和 加密用的cookie
    """
    INFO("gen cookies")
    params = {"area": "shouye_query_rec_hintq_rolling"}
    data = json.dumps({"appId": "24707", "params": json.dumps(params, ensure_ascii=False, separators=(",", ":"))},
                      separators=(",", ":"))
    get_cookie2(ps)
    get_api_resp(data, ps)
    get_cna(ps)


def get_next_page(resp, seed, app):
    """
    抓取翻页或者价格分组
    """

    def go_next_page():
        new_seed = {name: seed[name] for name in seed if name != "retry"}
        new_seed["page"] = new_seed.get("page", 1) + 1
        app.jq.lenqueue(new_seed)

    if seed.get("page", 1) > 1:
        # 已经翻页的条件分组直接继续翻页
        return go_next_page()

    # 当前是第一页需要判断是否需要按照价格分组
    start_price = seed.get("start_price", "")
    end_price = seed.get("end_price", "")
    total_result = resp["data"]["totalResults"]
    if int(total_result) < 2000:
        return go_next_page()

    if start_price == "" and end_price == "":
        pass


def parse_doc_h5(seed, info, reserve_price, sort_sale=False, currentPage=1, loc='', queryword=False):
    rg_ = seed.get('rg', 2.0)
    # 可以根据商品数阈值去选择是否分价格
    max_totalResults = seed.get('max_totalResults')
    min_price = seed.get('min_price', 0)
    max_price = seed.get('max_price', 999999)
    itemlist = info.get('itemsArray', [])
    has_next = True
    bsplit = False
    mid_price = None
    items = {
        'totalnum': 0,
        'items': [],
    }
    if info.get('totalPage') is None:
        return False, False, items, []
    elif int(info['totalPage']) == 0:
        return False, False, items, []
    else:
        totalnum = int(info.get('totalResults', 0))
        totalPage = int(info['totalPage'])
        if queryword == False and loc == '' and int(currentPage) == 1 and totalPage >= 200:
            rg = rg_ if queryword else 0.1
            mid_price = find_price_range(min_price, max_price, itemlist, reserve_price, rg=rg)
            if mid_price:
                bsplit = True
                has_next = False

        elif int(currentPage) == 1 and totalPage >= 200:
            INFO('_middle_price_invalid', itemlist[0], reserve_price, loc)
            # has_next = False
        if totalPage <= currentPage:
            has_next = False
        if max_totalResults and totalnum <= int(max_totalResults):
            bsplit = False

    INFO("seed:{},items:{}".format(seed, len(itemlist)))
    items = []
    for item in itemlist:
        item_id = item.get('item_id') or item.get('nid')
        if not item_id:
            continue
        try:
            title = item['title']
        except:
            try:
                titles = re.findall(
                    'show_title_structure:{\\"interest\\".*?"(.*?)\\"}|ss_stream_line_long_title:(.*?) | short_title:(.*?) | short_title:(.+)',
                    item['auction_ext'])[0]
            except:
                titles = re.findall('short_title:(.*?) ', item['auction_ext'])
            titles_l = []
            for title in titles:
                if title:
                    titles_l.append(title)
            if not titles_l:
                ERR('no_title, seed:%s, item.auction_ext:%s' % (seed, item['auction_ext']))
                titles_l = ['']
            titles_l.sort(key=lambda x: len(x))
            title = titles_l[0]
        try:
            img = item['pic_path']
        except:
            try:
                img = '//img.alicdn.com/imgextra/item' + item['sku_image_url_skulist']
            except:
                # 这样的类型不是商品
                if item.get('ext', {}).get('launchType') == "1":
                    continue
                else:
                    raise Exception('no_pic')
        try:
            uid = item['userId']
        except:
            uid = item['user_id']
        isB2c = item.get('isB2c', '')
        seller_types = re.findall('seller_type:(\d);', item.get('clickTrace', ''))
        if isB2c:
            seller_type = isB2c
        elif seller_types:
            seller_type = str(seller_types[0])
        elif uid == '725677994':
            seller_type = "1"
        else:
            ERR('get shop type error, item: %s' % (json.dumps(item)))
            raise Exception('no_shop_type')
        if seller_type != "1":
            shop_type = 'cshop'
        else:
            shop_type = 'tmall'
        price = item['price'] if item.get('price') else item['sku_discnt_price'].split('\x03')[0]
        price_type = 'price' if item.get('price') else 'sku_discnt_price'
        pro_price = item.get('priceWithRate', price)
        ww = item.get('nick', '')
        loc = item.get('location', '')
        comment = item.get('commentCount', '')
        try:
            if not item.get('sold'):
                clicktrace_sold = re.findall('sold:(\d+)', item.get('clickTrace', ''))
                if clicktrace_sold:
                    sold = int(clicktrace_sold[0])
                else:
                    sold = 0
            else:
                sold = int(item.get('sold', '0'))
        except:
            # tmcs商品没有销量
            sold = 0
        back_cid = item.get('category', '')
        clickTrace = item.get('clickTrace')
        # 传进来的是后台cid，没有前台cid
        cid = ''
        iconList = []
        if uid != '725677994':
            iconList = item.get("iconList", '').split(',')
        is_global = True if 'quanqiugou' in iconList else False
        item_ = {
            'item_id': str(item_id),
            'title': str(title),
            'pic': str(img),
            'price': str(price),
            'pro_price': str(pro_price),
            'sold': sold,
            'buy_count': sold,
            'ww': ww,
            'uid': str(uid),
            'loc': loc,
            'comment': comment,
            'shop_type': shop_type,
            'back_cid': str(back_cid),
            'cid': cid,
            'brand_id': None,
            'clickTrace': str(clickTrace),
            'crawl_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'seed': seed,
            'price_type': price_type,
            'iconList': iconList,
            'is_global': is_global,
        }
        # 对字段值类型进行qa
        field_type_qa('cat_items', item_)
        items.append(item_)

    if sort_sale and len(items) > 0 and currentPage < totalPage:
        try:
            allsold = sum([x['sold'] for x in items])
            # if int(items[0]['sold']) == 0:
            if allsold == 0:
                has_next = False
            else:
                has_next = True
                # pass
        except Exception, e:
            ERR('sum all items sold error.', e)
            # pass
    items = {
        'totalnum': totalnum,
        'items': items,
    }
    return bsplit, has_next, items, mid_price


def get_items(seed, app, ps):
    if "cna" not in ps.session.cookies.get_dict():
        gen_cookie(ps)
    keyword = seed.get("q", "")
    cid = seed.get("cid", "")
    pageno = seed.get('pageno', 1)
    is_tmall = seed.get('is_tmall', False)
    tab = 'newmall' if is_tmall else 'all'
    reserve_price = seed.get('reserve_price')
    loc = seed.get('loc', '')
    sort_ = seed.get('sort', '_sale')
    if reserve_price:
        start_price, end_price = reserve_price
    else:
        start_price = ''
        end_price = ''
    if loc != '':
        if type(loc) == unicode:
            loc = loc.encode('utf-8')
    params = OrderedDict(
        {"isBeta": "false", "grayHair": "false", "appId": "29859", "from": "nt_history", "brand": "HUAWEI",
         "info": "wifi", "index": "4", "ttid": "600000@taobao_android_10.7.0", "needTabs": "true", "rainbow": "",
         "areaCode": "CN", "vm": "nw", "schemaType": "auction", "elderHome": "false", "device": "HMA-AL00",
         "isEnterSrpSearch": "true", "newSearch": "false", "network": "wifi", "subtype": "",
         "hasPreposeFilter": "false", "client_os": "Android", "gpsEnabled": "false", "searchDoorFrom": "srp",
         "debug_rerankNewOpenCard": "false", "homePageVersion": "v7", "start_price": start_price,
         "end_price": end_price, "loc": loc,
         "searchElderHomeOpen": "false", "style": "wf", "page": pageno, "n": "10", "q": keyword, "cat": cid,
         "search_action": "initiative", "sugg": "_4_1", "m": "h5", "sversion": "13.6", "prepositionVersion": "v2",
         "tab": tab, "tagSearchKeyword": None, "sort": sort_, "filterTag": "", "prop": ""})

    params = json.dumps(params, ensure_ascii=False, separators=(",", ":"))
    data = json.dumps({"appId": "29859", "params": params}, ensure_ascii=False, separators=(",", ":"))
    resp = get_api_resp(data, ps)
    ret = "".join(resp.get("ret", ""))
    if "SUCCESS" in ret:
        return resp
    elif "FAIL_SYS_TOKEN_EXOIRED" in ret:
        # 令牌过期
        raise Exception("FAIL_SYS_TOKEN_EXOIRED")
    elif "RGV587_ERROR" in ret and "login.taobao.com/member" in resp.get("data", {}).get("url", ""):
        # 需要登录
        INFO("seed:{},login needed".format(seed))
        ps.session.cookies.clear()
        raise Exception("RGV587_ERROR")
    else:
        ERR("ret:{}".format(ret))
        raise Exception(ret.split(':')[0])


def cat_items(seed, app, ps):
    """
    类目搜索入口
    seed 中必须要有q,表示搜索的关键词， page表示页数，默认第一页
    最大翻页到200,继续翻页返回第200页的数据
    """
    q = seed.get("q", "")
    pageno = seed.get('pageno', 1)
    reserve_price = seed.get('reserve_price')
    loc = seed.get('loc', '')
    sort_ = seed.get('sort', '_sale')
    resp = get_items(seed, app, ps)
    qword = (q != "")
    need_price_split, next_page, items, mid_price = parse_doc_h5(
        seed, resp["data"], reserve_price, sort_, pageno, loc, queryword=qword)
    items = items['items']
    if pageno == 1 and not items:
        INFO('page1_not_items', json.dumps(seed))
    thisitems = [x['item_id'] for x in items]
    if seed.get('pre_items'):
        dup_items = list(set(seed['pre_items']) & set(thisitems))
        if len(dup_items) > 5:
            ERR('dupitems', seed, thisitems, dup_items)
            raise Exception('dupitems')
    seed['pre_items'] = thisitems
    # return items
    if need_price_split:
        INFO('split', mid_price, seed)
        if reserve_price is None:
            reserve_price = ['', '']
        if mid_price is None and seed.get('is_loc', True):
            # 最小的价格,页数也大于100，需要按区域爬取
            INFO('locs crawler', seed, reserve_price)
            for loc in locs:
                seed2 = seed.copy()
                seed2['pageno'] = 1
                seed2['loc'] = loc
                seed2['retry'] = 0
                app.jq.enqueue(seed2)
            return items
        front = [reserve_price[0], str(mid_price)]
        back = [str(mid_price + 0.01), reserve_price[1]]
        # INFO('middle_price', front, back)
        if check_price_range(front):
            seed2 = seed.copy()
            seed2['pageno'] = 1
            seed2['reserve_price'] = front
            seed2['retry'] = 0
            app.jq.enqueue(seed2)

        if check_price_range(back):
            seed2 = seed.copy()
            seed2['pageno'] = 1
            seed2['reserve_price'] = back
            seed2['retry'] = 0
            app.jq.enqueue(seed2)

        return items
    # 支持是否翻页爬取
    if seed.get('is_next_page', True) and next_page and seed['pageno'] < 200:
        # items = content
        seed['pageno'] += 1
        seed['retry'] = 0
        app.jq.lenqueue(seed)
    return items


def prepare_run(jq):
    jq.reset()
    seed = {"q": "饼干", "type": "cat_items"}
    jq.enqueue(seed)


def prepare_word(jq):
    import pymongo
    jq.reset()
    now = (datetime.datetime.now() - datetime.timedelta(days=1)
           ).strftime('%Y_%-m_%-d')
    now = '2020_5_21'
    # db = pymongo.MongoClient('dbredis').supportdb
    db = pymongo.MongoClient('192.168.198.173').supportdb
    words = [u'馋匪', u'轩妈', u'每日黑巧', u'nocclili旗舰店', u'moti']
    for q in words:
        jq.enqueue(
            json.dumps({
                'q': q,
                'pageno': 1,
                'type': 'cat_items',
                'need_price_split': False,
                'b64': 1,
            }))

    for r in db['wordstats_%s' % now].find({
        'dup': {
            '$ne': 1
        },
        'ignore': {
            '$ne': 1
        }
    }):
        if r.get('pvi') > 2000 and len(r['word']) > 1 and len(r['word']) < 10:
            jq.enqueue(
                json.dumps({
                    'q': r['word'],
                    'pageno': 1,
                    'type': 'cat_items',
                    'need_price_split': False,
                    'b64': 1,
                }))
            jq.enqueue(
                json.dumps({
                    'q': r['word'],
                    'pageno': 1,
                    'type': 'cat_items',
                    'need_price_split': False,
                    'b64': 1,
                    'is_tmall': True
                }))


def test1():
    from moojing.spiderman.page import get_random_spider
    import threading
    ps = get_random_spider(typ='rproxy', user_agent_type='mobile')
    gen_cookie(ps)
    # "_sale" if sort_sale else "_coefp"
    seed = {
        # 'q': u'每日黑巧==',
        # 'q': u'花花公子旗舰店',
        'q': u'预售',
        'pageno': 1,
        'type': 'cat_items',
        'is_tmall': True,
    }
    # seed = {"pageno": 1, "ignoreflood": True, "q": "\u7406\u8d22", "utdid": None, "type": "cat_items", "pre_items": ["595800647737", "571155190662", "578173045845", "607717435369", "639100798919", "625838323863", "618608756659", "625612012447", "603391292899", "528375113705", "608162152567", "612197722573", "636919260139", "575209112393", "616516751457", "634316984162", "591426009639", "636713417846", "627553504570", "623728932533"]}
    seed = {"brand_ppath": "", "is_tmall": False, "pageno": 1, "cid": "50007068", "reserve_price": ["", "499999.0"]}
    # seed = {"retry": 50, "pageno": 1, "b64": "1", "ignoreflood": True, "q": "全球购", "need_price_split": False, "type": "cat_items"}
    # seed = {"brand_ppath": "", "retry": 50, "pageno": 1, "cid": "50066815", "ignoreflood": True, "reserve_price": ["0", "3784.18"], "type": "cat_items"}
    app = threading.local()
    app.ps = ps
    # seed['reserve_price'] = ['100', '110']
    # seed['loc'] = '广西'
    # seed['utdid'] = generate_utdid()

    for i in range(100):
        try:
            # seed['pageno'] = i + 1
            r = cat_items(seed, app, app.ps)[:20]
            print
            json.dumps(r)
            print
            'aaaaaaaa', i, len(r)
            for item in r:
                print
                item['item_id'], item['title'], item['pro_price'], item['sold'], item['comment']
            # break
            time.sleep(3)
            return
        except Exception, e:
            print
            e
            import traceback
            print
            traceback.format_exc()
            break
            if 'location' in str(e):
                break


if __name__ == '__main__':
    worker = BasicWorker(project='catappitems', proxy_type='rproxy', user_agent_type='mobile', sleep_time=5,
                         active_interval=60 * 15)
    worker.run()
    #111