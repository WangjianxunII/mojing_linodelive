# coding:utf-8
import requests
from collections import OrderedDict
import json
import urllib
import sys

import urllib3.util.ssl_
import requests
# 处理协议 修改加密套件
urllib3.util.ssl_.DEFAULT_CIPHERS = ":".join(
    [i for i in urllib3.util.ssl_.DEFAULT_CIPHERS.split(":") if not i.startswith("!")][:-2])

from requests import Session
from hyper.contrib import HTTP20Adapter
from requests.utils import CaseInsensitiveDict

_request = Session.request


class MyHTTP20Adapter(HTTP20Adapter):
    def __init__(self, *args, **kwargs):
        super(MyHTTP20Adapter, self).__init__(*args, **kwargs)
        super(HTTP20Adapter, self).__init__(*args, **kwargs)


def request(self, method, url, clear_headers=False, http2=False, **kwargs):
    # 处理http2请求
    if http2:
        self.mount("https://", MyHTTP20Adapter())
    # 处理 headers顺序 这里采用的方法取删除默认的headers 传入的headers就是最终的headers
    if clear_headers:
        self.headers = CaseInsensitiveDict()
    result = _request(self, method=method, url=url, **kwargs)
    return result


Session.request = request

session = Session()

from hashlib import md5
import time

url = "https://main.m.taobao.com/"
proxies = {"http": "http://hades.p.shifter.io:20759","https": "http://hades.p.shifter.io:20759"}
# proxies = None
# proxies = {"https":"http://127.0.0.1:8888"}

import logging
logging.basicConfig(level=logging.DEBUG, format="%(message)s")
logger = logging.getLogger()


def get_cna(session):
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
        try:
            url = "https://log.mmstat.com/eg.js?t={}".format(int(time.time() * 1000))
            session.get(url, headers=headers, proxies=proxies, timeout=30)
            if "cna" in session.cookies.get_dict():
                break
        except Exception as e:
            print 'ad:',e
            continue
    else:
        # raise Exception("get_cna_failed")
        try:
            raise Exception("get_cna_failed")
        except Exception as e:
            print e



def get_cookie2(ps):
    headers = {
        'authority': 'login.m.taobao.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'zh-CN,zh;q=0.9',
    }
    for i in range(10):
        url = "https://login.m.taobao.com/login.htm"
        try:
            session.get(url, headers=headers, proxies=proxies, timeout=30)
        except:
            continue
        if "cookie2" in session.cookies.get_dict():
            break
        else:
            try:
                raise Exception("get_cookie2_failed")
            except Exception as e:
                print e






def get_api_resp(data, session):
    """
    封装的请求 mtop.relationrecommend.WirelessRecommend.recommend, data 有两种格式
    """
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'script',
        'Referer': 'https://main.m.taobao.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    cookies = session.cookies.get_dict()
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
    url = "https://h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/?" + urllib.urlencode(post_data)
    for i in range(10):
        try:
            resp = session.get(url, headers=headers, proxies=proxies, verify=False, cookies=cookies, timeout=40)
            break
        except:
            continue

def gen_cookie():
    """
    获取cookie,cna 和 加密用的cookie
    """
    print 111
    session = requests.session()
    params = {"area": "shouye_query_rec_hintq_rolling"}
    data = json.dumps({"appId": "24707", "params": json.dumps(params, ensure_ascii=False, separators=(",", ":"))},
                      separators=(",", ":"))
    get_cookie2(session)
    get_api_resp(data,session)
    get_cna(session)
    cookeis = session.cookies.get_dict()
    return cookeis


def get_sign(token, timestamp, data):
    """
    淘宝h5接口签名sign计算
    :param timestamp: 13位时间戳
    :param data: 接口发送的参数 data str
    """
    text = '{}&{}&12574478&{}'.format(token, timestamp, data)
    result = str(md5(text).hexdigest())
    return result


params = (
    ('jsv', '2.6.2'),
    ('appKey', '12574478'),
    ('t', '1647573970900'),
    ('sign', 'd398ee5bd469e4d60ca93f9222dff221'),
    ('api', 'mtop.relationrecommend.WirelessRecommend.recommend'),
    ('v', '2.0'),
    ('type', 'jsonp'),
    ('dataType', 'jsonp'),
    ('callback', 'mtopjsonp1'),
    ('data', '{"appId":"24707","params":"{\\"area\\":\\"shouye_query_rec_hintq_rolling\\"}"}'),
)


allitemsdep = set()

def get(data, cookies=None):
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'script',
        'Referer': 'https://main.m.taobao.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # "Cookie":"cna=nzzAGts9W0gCAd9oJ0gVm0ny; _m_h5_tk=ca17068e59dd800ed0550233884e425c_1647932927208; _m_h5_tk_enc=f8288bd908d3b00e63ea4aba9d367319; cookie2=16b556320b5160a25dbd93c2e44efd1c",
    }
    session_cookies = session.cookies.get_dict()
    if cookies:
        cookies.update(session_cookies)
    else:
        cookies = session_cookies
    token = cookies.get("_m_h5_tk")
    token = "" if token is None else token.split("_")[0].strip()
    # token = "ca17068e59dd800ed0550233884e425c"
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
    headers["Referer"] = "https://main.m.taobao.com/search/index.html?pageType=3&q={}".format(seed["keyword"])
    resp = session.get(url, headers=headers, proxies=proxies, verify=False, cookies=cookies)
    data = resp.text.split("(",1)[1].strip(") ")
    # print(data)
    data = json.loads(data)
    items = data.get("data",{}).get("itemsArray",[])
    if len(items) == 0 :
        print(json.dumps(data))
    itemids = []
    repeat = 0
    for item in items:
        item_id = item["item_id"] if "item_id" in item else item["nid"]
        if item_id in allitemsdep:
            print("item_id:{} repeat".format(item_id))
            repeat = 1
        allitemsdep.add(item_id)
        itemids.append(item_id)
        price = item.get("sku_discnt_price") if "sku_discnt_price" in item else item.get("priceWithRate")
        da = u"title:{},item_id:{},price:{},category:{},sales:{}".format(item.get("title"),item_id,price,item.get("category"),item.get("sold"))
        # da = "title:{},item_id:{},price:{},category:{},sales:{}".format(item.get("title"),item_id,price,item.get("category"),item.get("sold"))
        logger.info(da)

        with open('content213.txt', 'a+') as f:
            f.write(da.encode('utf-8')+'\n')

    if repeat:
        raise Exception("repeat")
    return data,itemids

seed = {"keyword":""}
def get_page(page,prefix,itemsids=""):
    logger.info("page:{}".format(page))
    params = OrderedDict(
        {"isBeta": "false", "grayHair": "false", "appId": "29859", "from": "nt_history", "brand": "HUAWEI",
         "info": "wifi", "index": "4", "ttid": "600000@taobao_android_10.7.0", "needTabs": "true", "rainbow": "",
         "areaCode": "CN", "vm": "nw", "schemaType": "auction", "elderHome": "false", "device": "HMA-AL00",
         "isEnterSrpSearch": "true", "newSearch": "false", "network": "wifi", "subtype": "",
         "hasPreposeFilter": "false", "client_os": "Android", "gpsEnabled": "false", "searchDoorFrom": "srp",
         "debug_rerankNewOpenCard": "false", "homePageVersion": "v7",
         "searchElderHomeOpen": "false", "style": "wf", "page": page ,"n": "10", "q": "防尘塞","cat":"",
         "search_action": "initiative", "sugg": "_4_1", "m": "h5", "sversion": "13.6", "prepositionVersion": "v2",
         "tab": "all", "tagSearchKeyword": None, "sort": "_sale", "filterTag": "", "prop": ""})

    # params = OrderedDict(
    #     {"appId": "29859", "from": "nt_history", "brand": "HUAWEI",
    #      "info": "wifi", "index": "4", "ttid": "600000@taobao_android_10.7.0", "needTabs": "true", "rainbow": "",
    #      "areaCode": "CN", "vm": "nw", "schemaType": "auction", "elderHome": "false", "device": "HMA-AL00",
    #      "isEnterSrpSearch": "false", "newSearch": "false", "network": "wifi", "subtype": "",
    #      "hasPreposeFilter": "false", "client_os": "Android", "gpsEnabled": "false", "searchDoorFrom": "srp",
    #      "debug_rerankNewOpenCard": "false", "homePageVersion": "v7", "searchElderHomeOpen": "false", "style": "wf",
    #      "page": page, "n": "10", "q":"","search_action": "initiative", "sugg": "_4_1", "m": "app",
    #      "sversion": "13.6", "prepositionVersion": "v2", "tab": "all", "channelSrp": "newh5", "tagSearchKeyword": None,
    #      "sort": "_sale", "filterTag": "", "prop": "", "catmap":"50103041",
    #      "itemIds": itemsids,"itemS": (page-1) *10
    #      }
    # )

    # params = OrderedDict(
    #     {"isBeta": "false", "grayHair": "false", "appId": "29859", "from": "nt_history", "brand": "HUAWEI",
    #      "info": "wifi", "index": "4", "ttid": "600000@taobao_android_10.7.0", "needTabs": "true", "rainbow": "",
    #      "areaCode": "CN", "vm": "nw", "schemaType": "auction", "elderHome": "false", "device": "HMA-AL00",
    #      "isEnterSrpSearch": "true", "newSearch": "false", "network": "wifi", "subtype": "",
    #      "hasPreposeFilter": "false", "client_os": "Android", "gpsEnabled": "false", "searchDoorFrom": "srp",
    #      "debug_rerankNewOpenCard": "false", "homePageVersion": "v7", "searchElderHomeOpen": "false", "style": "wf",
    #      "page": page, "n": "10", "q": "防尘塞", "search_action": "initiative", "sugg": "_4_1", "m": "h5", "sversion": "13.6",
    #      "prepositionVersion": "v2", "tab": "all", "channelSrp": "newh5", "tagSearchKeyword": None, "sort": "_sale",
    #      "filterTag": "", "prop": "", "itemIds": "", "itemS": (page-1) *10}
    # )
    # 
    # params = OrderedDict(
    #     {"isBeta": "false", "grayHair": "false", "appId": "29859", "from": "nt_history", "brand": "HUAWEI",
    #      "info": "wifi", "index": "4", "ttid": "600000@taobao_android_10.7.0", "needTabs": "true", "rainbow": "",
    #      "areaCode": "CN", "vm": "nw", "schemaType": "auction", "elderHome": "false", "device": "HMA-AL00",
    #      "isEnterSrpSearch": "true", "newSearch": "false", "network": "wifi", "subtype": "",
    #      "hasPreposeFilter": "false", "client_os": "Android", "gpsEnabled": "false", "searchDoorFrom": "srp",
    #      "debug_rerankNewOpenCard": "false", "homePageVersion": "v7", "searchElderHomeOpen": "false", "style": "wf",
    #      "page": page, "n": "10", "q": "", "search_action": "initiative", "sugg": "_4_1", "m": "h5", "sversion": "13.6",
    #      "prepositionVersion": "v2", "tab": "all", "channelSrp": "newh5", "loc": "", "service": "", "prop": "",
    #      "end_price": "", "start_price": "", "catmap": "50018621", "tagSearchKeyword": None, "sort": "_sale",
    #      "filterTag": "50018621"}
    # )
    # _sale
    params = json.dumps(params, ensure_ascii=False, separators=(",", ":"))
    print params
    data = json.dumps({"appId": "29859", "params": params}, ensure_ascii=False, separators=(",", ":"))

    items,itemids = get(data, cookies=cookies)

    return itemids


if __name__ == "__main__":
    # if len(sys.argv) > 1:
    #     get_page(int(sys.argv[1]), "default_requests_params_cats")
    #     page = sys.argv[1]
    # else:
    #     import subprocess
    #     # for page in range(201,300):
    #     for i in range(1,200):
    #         subprocess.check_output("python test.py {}".format(i))
    #         # time.sleep(10)
    # get_page(6,"default_requests_params_cats_shoudong")
    # cookies = {
    #     'cna': 'lDTAGmVEd0cCAd9oJ3s2lnwL',
    #     # 'miid': '6029581491429530031',
    #     # 'lgc': '%5Cu7F8E%5Cu675C%5Cu838E%5Cu548C%5Cu7F8E%5Cu675C%5Cu7F57',
    #     # 'tracknick': '%5Cu7F8E%5Cu675C%5Cu838E%5Cu548C%5Cu7F8E%5Cu675C%5Cu7F57',
    #     # '_cc_': 'UtASsssmfA%3D%3D',
    #     # 'thw': 'cn',
    #     # 'enc': 'ypFUmHyejcwRpZT4yn42L8bfAky54ccRDptFJGr0Td0Wf6xLBCcLA4dYzSEs5hYP5gXlvnyqyjogSuudRtOcTA%3D%3D',
    #     # 't': '31d65b12c27abfa551c8fd9c7536cfac',
    #     # 'sgcookie': 'E100yx9eDyM7KhWJnRUs8lqB3FnAjlTfzdXlLjUNnHEBaBE4eVJ0Sdkaw2fvn7fwwpxSOGd44sr05C0ijR%2BOQYTZsU6IcOiq%2Bjzr1CLp%2BahV3Wz2zgm9z6qmsweRkYb1roKC',
    #     # 'uc3': 'lg2=VFC%2FuZ9ayeYq2g%3D%3D&vt3=F8dCvCh0857LsJjrFk0%3D&id2=UU6hRiHjBYpRsQ%3D%3D&nk2=oHpU%2FMQV1Vw7pGTpt4A%3D',
    #     # 'uc4': 'id4=0%40U2xsBh9YrBMuw9kH7bwHFcYUlHUs&nk4=0%40oijSy3iq9ZVgrPDXlvNDlfNGiv3H2Qaeyg%3D%3D',
    #     # 'mt': 'ci=3_1',
    #     # 'tfstk': 'c4L5Buq-U827WbiUzQGq8eMsFRbdCmV1O06kNxaJKAqjJSGlny1mLPWsnZ-3pw5dG',
    #     # 'l': 'eBjidETlLsWxqyP1BOfZlurza77TDIRAguPzaNbMiOCPOYfBR6RdB62YtPL6CnGVh6zvR3WK4ADXBeYBqHKKnxvTzmyFkCDmn',
    #     '_m_h5_tk': 'd4f1d0205f1d31af82780eb80f8be8c1_1650005225100',
    #     '_m_h5_tk_enc': '0dedd13260c86c884cea659b9b413b48',
    #     # 'isg': 'BBERRj0xF3cNeHsHamTLRaA4IB2rfoXwzkjR-vOiAFgSmjDsOsq0wcm8PG58kh0o',
    # }
    # title: 趣多多大块曲奇饼干黑巧克力味营养早餐网红休闲零食144g食品, item_id: 623590269511, price: 13.90, category: 124302001, sales: None
    # title: 饼干200g整箱爆浆曲奇小丸子, item_id: 645082319658, price: 15.80, category: None, sales: 63887
    # title: 趣多多爆逗曲奇粒粒巧克力味96g大块巧克力饼干网红零食曲奇饼干, item_id: 641821677713, price: 30.0030.0060.00, category: 124302001, sales: None
    # title: 百草味蔓越莓曲奇饼干零食小吃, item_id: 44800690064, price: 6.50, category: None, sales: 41400
    # title: 百草味手工点心蔓越莓曲奇网红, item_id: 42106811504, price: 18.90, category: None, sales: 27059
    # title: 曲奇独立包装饼干零食, item_id: 619040171970, price: 29.90, category: None, sales: 22395
    # title: 趣多多曲奇巧克力味饼干早餐速食网红休闲儿童办公室小零食170g, item_id: 623864694989, price: 23.90, category: 124302001, sales: None
    # title: 趣多多香脆礼盒装儿童曲奇饼干, item_id: 598439456837, price: None, category: None, sales: 18468
    # title: 好吃点饼干可爱熊字饼115g休闲食品儿童营养酥脆饼干零食点心小吃, item_id: 12472919348, price: 2.902.90, category: 124302001, sales: None
    # title: 夹心饼干爆浆下午茶曲奇蔓越莓, item_id: 619162735760, price: 9.90, category: None, sales: 21442
    cookies = gen_cookie()
    print cookies
    # cookies = {'_m_h5_tk_enc': 'b614bca4d2a6e2b4e453aad23c2dd67e', '_m_h5_tk': '5dd106d8a2e500ace7c959b1566ba725_1650265144046', 'cna': 'q9XjGuba2lACAbockE7gmX/8'}
    # cookies = {
    #     'cna': '/RbcGaCobjQCAXLyIXcnivg+',
    #     'WAPFDFDTGFG': '%2B4cMKKP%2B8PI%2Bu6jNGXoNESTzlpfErSNMldm4zNGVjQU%3D',
    #     '_w_app_lg': '0',
    #     'tracknick': '%5Cu7F8E%5Cu675C%5Cu838E%5Cu548C%5Cu7F8E%5Cu675C%5Cu7F57',
    #     'thw': 'cn',
    #     't': '9d9948d5f9f36a97c28b7d496874c266',
    #     '_m_h5_tk': '69c1d408b689cd48f363a3c8d94c838d_1650265354045',
    #     '_m_h5_tk_enc': '19e8288bdcb902cef95624bdcc039c7b',
    #     '_samesite_flag_': 'true',
    #     'cookie2': '10dd68ce9b1fae9756394808fc410499',
    #     '_tb_token_': 'e68373b8b5e56',
    #     'xlly_s': '1',
    #     'sgcookie': 'E100CRML%2FJTuLEqfDxuOFLfbFZCDD7D3fYfH9zPyyNLEOutSwhpjU10Ckbs%2BO7fyUkuoftwjNThRWIoIRpDzjeHV8EVw2fSePosaeENm6LklBYKV%2FWJCy5PVHMmR%2BrP5EjHa',
    #     'ockeqeudmj': 'tsUp3Mw%3D',
    #     '_w_tb_nick': '%E7%BE%8E%E6%9D%9C%E8%8E%8E%E5%92%8C%E7%BE%8E%E6%9D%9C%E7%BD%97',
    #     'munb': '2602165130',
    #     'unb': '2602165130',
    #     'uc3': 'vt3=F8dCvCh89yTQUYYmcQs%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D&nk2=oHpU%2FMQV1Vw7pGTpt4A%3D&id2=UU6hRiHjBYpRsQ%3D%3D',
    #     'uc1': 'existShop=false&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&cookie14=UoexMn5uVSgPug%3D%3D&cookie21=VT5L2FSpdeCjwGS%2FFqZpWg%3D%3D',
    #     'csg': '563e6766',
    #     'lgc': '%5Cu7F8E%5Cu675C%5Cu838E%5Cu548C%5Cu7F8E%5Cu675C%5Cu7F57',
    #     'ntm': '0',
    #     'cancelledSubSites': 'empty',
    #     'cookie17': 'UU6hRiHjBYpRsQ%3D%3D',
    #     'dnk': '%5Cu7F8E%5Cu675C%5Cu838E%5Cu548C%5Cu7F8E%5Cu675C%5Cu7F57',
    #     'skt': 'bde68712e1373974',
    #     'uc4': 'nk4=0%40oijSy3iq9ZVgrPDXlvNDlfNHgmajsRLjtg%3D%3D&id4=0%40U2xsBh9YrBMuw9kH7b2oRr072k7n',
    #     '_cc_': 'UtASsssmfA%3D%3D',
    #     '_l_g_': 'Ug%3D%3D',
    #     'sg': '%E7%BD%9704',
    #     '_nk_': '%5Cu7F8E%5Cu675C%5Cu838E%5Cu548C%5Cu7F8E%5Cu675C%5Cu7F57',
    #     'cookie1': 'B0ADLuVm01eV3zl5Kr10vD%2FnP1HXPNt85sKCDAJ3ZaM%3D',
    #     'tfstk': 'c9qFBgGFDDJzGco5kDiPNLcbem3daurgAskK-sqW8GZ9gB3ngsmpwAbW-rzvyg3h.',
    #     'l': 'eBaQl9XegiFxyKdZBOfZrurza7rEjIREIuPzaNbMiOCP9MCH5hZFW62dzmYMCnNRnsQkj35i5nQgBjTLryzBQxv9-eM_P-ionddC.',
    #     'isg': 'BF5e4N8OsNUO6-c4EK3BKcaBr_agHyKZQlEZ5Qjny6GEK_wFcK9tqdHNJ3GCIhqx',
    # }

    # cookies = {'_m_h5_tk_enc': '6b2b5366c46df176fa1fe63c786b24ec', '_m_h5_tk': '86649500148ad058273b3b11dbc2c4bf_1650012924183', 'cna': 'pQDgGtm2gWoCAWB+Z0PlLWb0'}
    # cookies = {'_m_h5_tk_enc': 'cf1d60d48bffee3e07155e29c80734aa', '_m_h5_tk': 'f39cc2f0eea23422aed5c068ae97e511_1650022553915', 'cna': '+QvgGrqDBT0CAVZ8Siu26da0'}
    print(cookies)
    items= []
    # get_page(134, "dddsda", ",".join(items))
    for i in range(1,201):
        for j in range(200):
            try:
                get_page(i, "dddsda",",".join(items))
                # time.sleep(3)
                break
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                continue
        # time.sleep(3)
    print(len(allitemsdep))

    # def th_get_page(page,prefix,itemsids):
    #
    #     try:
    #         get_page(page,prefix,itemsids)
    #     except:
    #         pass
    #
    # items = []
    # import threading
    # pools = []
    # # items = get_page(7, "code_cookie", ",".join(items))
    # for page in range(1,200):
    #     p = threading.Thread(target=th_get_page,kwargs={"page":page,"prefix":"11","itemsids":""})
    #     pools .append(p)
    #     p.start()
    # for p in pools:
    #     p.join()
    # print(len(allitemsdep))
#


# 服务器和本地限速3s 1。服务器 2。本地
# 1。
# 去重前 抓取数据： 2110,2500,2000,2000,2000
# 去重后 抓取数据： 2000,2000,2000,2000,2000
# 2。
# 去重前 抓取数据： 2239,2120,2000,2030,2019,2070
# 去重后 抓取数据： 2129,2000,2000,2000,1989,2000
#
# 服务器和本地不限速限速 1。服务器 2。本地
# 1。
# 去重前 抓取数据： 1999,2460,2080,2000,2050
# 去重后 抓取数据： 1999,2009,2000,2000,2000
# 2。
# 去重前 抓取数据： 2020,1700,2000,2060,1910,2000
# 去重后 抓取数据： 2000,1620,2000,2000,1910,2000
#
# 服务器 不带cid
# 去重前 抓取数据： 490465
# 去重后 抓取数据： 24484

# mac ua
# 去重前 抓取数据： 3560
# 去重后 抓取数据： 2339
# win ua
# 去重前 抓取数据： 3210
# 去重后 抓取数据： 2415
# 手机 ua-safari
# 去重前 抓取数据： 2000，2000
# 去重后 抓取数据： 2000，2000
# 手机 ua-Google
# 去重前 抓取数据： 2000，2000
# 去重后 抓取数据： 2000，2000
