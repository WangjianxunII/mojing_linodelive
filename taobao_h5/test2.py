# coding:utf-8
import random

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

def abuyun_proxy():
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "H7ODW0OGV50UH6ED"
    proxyPass = "A30B3B2097937505"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }

    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    return proxies

def Random_UA():
    UA = [
        'Mozilla/5.0 (Linux; U; Android 9; zh-CN; MI 8 SE Build/PKQ1.181121.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 Quark/3.0.4.945 Mobile Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 SP-engine/2.22.0 main%2F1.0 baiduboxapp/11.26.1.10 (Baidu; P2 13.5.1) NABar/1.0 webCore=0x1327ad770',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 10; STK-AL00; HMSCore 5.0.4.301) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 HuaweiBrowser/11.0.4.300 Mobile Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 SP-engine/2.23.0 main%2F1.0 baiduboxapp/12.0.0.11 (Baidu; P2 13.5.1) NABar/1.0 webCore=0x12c507de0',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/13.0 MQQBrowser/9.4.0 Mobile/15B87 Safari/604.1 MttCustomUA/2 QBWebViewType/1 WKType/1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 SP-engine/2.22.0 main%2F1.0 baiduboxapp/11.26.1.10 (Baidu; P2 13.6) NABar/1.0 webCore=0x12bb8f7f0',
        'Mozilla/5.0 (Linux; Android 10; LYA-AL00 Build/HUAWEILYA-AL00L; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/11.15 baiduboxapp/11.15.5.10 (Baidu; P1 10)',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.4(0x17000820) NetType/4G Language/zh_CN',
        'Mozilla/5.0 (Linux; U; Android 10; zh-CN; PBET00 Build/QKQ1.190918.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Quark/4.6.1.159 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; U; Android 10; zh-cn; MI 9 Transparent Edition Build/QKQ1.190825.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/11.1 Mobile Safari/537.36 COVC/045429',
        'Mozilla/5.0 (Linux; U; Android 11; zh-cn; PDHM00 Build/RKQ1.200710.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/11.2 Mobile Safari/537.36 COVC/045517',
        'Mozilla/5.0 (Linux; Android 11; SM-G9860) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; U; Android 11; zh-cn; Mi9 Pro 5G Build/RKQ1.200826.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/79.0.3945.147 Mobile Safari/537.36 XiaoMi/MiuiBrowser/13.7.15',
          ]
    UA = [
        'Mozilla/5.0 (Linux; U; Android 9; zh-CN; MI 8 SE Build/PKQ1.181121.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 Quark/3.0.4.945 Mobile Safari/537.36',
          ]
    return random.choice(UA)
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
Proxies_list = [{'http': 'http://hades.p.shifter.io:20740', 'https': 'http://hades.p.shifter.io:20740'}, {'http': 'http://hades.p.shifter.io:20741', 'https': 'http://hades.p.shifter.io:20741'}, {'http': 'http://hades.p.shifter.io:20742', 'https': 'http://hades.p.shifter.io:20742'}, {'http': 'http://hades.p.shifter.io:20743', 'https': 'http://hades.p.shifter.io:20743'}, {'http': 'http://hades.p.shifter.io:20744', 'https': 'http://hades.p.shifter.io:20744'}, {'http': 'http://hades.p.shifter.io:20745', 'https': 'http://hades.p.shifter.io:20745'}, {'http': 'http://hades.p.shifter.io:20746', 'https': 'http://hades.p.shifter.io:20746'}, {'http': 'http://hades.p.shifter.io:20747', 'https': 'http://hades.p.shifter.io:20747'}, {'http': 'http://hades.p.shifter.io:20748', 'https': 'http://hades.p.shifter.io:20748'}, {'http': 'http://hades.p.shifter.io:20749', 'https': 'http://hades.p.shifter.io:20749'}, {'http': 'http://hades.p.shifter.io:20750', 'https': 'http://hades.p.shifter.io:20750'}, {'http': 'http://hades.p.shifter.io:20751', 'https': 'http://hades.p.shifter.io:20751'}, {'http': 'http://hades.p.shifter.io:20752', 'https': 'http://hades.p.shifter.io:20752'}, {'http': 'http://hades.p.shifter.io:20753', 'https': 'http://hades.p.shifter.io:20753'}, {'http': 'http://hades.p.shifter.io:20754', 'https': 'http://hades.p.shifter.io:20754'}, {'http': 'http://hades.p.shifter.io:20755', 'https': 'http://hades.p.shifter.io:20755'}, {'http': 'http://hades.p.shifter.io:20756', 'https': 'http://hades.p.shifter.io:20756'}, {'http': 'http://hades.p.shifter.io:20757', 'https': 'http://hades.p.shifter.io:20757'}, {'http': 'http://hades.p.shifter.io:20758', 'https': 'http://hades.p.shifter.io:20758'}, {'http': 'http://hades.p.shifter.io:20759', 'https': 'http://hades.p.shifter.io:20759'}, {'http': 'http://hades.p.shifter.io:20760', 'https': 'http://hades.p.shifter.io:20760'}, {'http': 'http://hades.p.shifter.io:20761', 'https': 'http://hades.p.shifter.io:20761'}, {'http': 'http://hades.p.shifter.io:20762', 'https': 'http://hades.p.shifter.io:20762'}, {'http': 'http://hades.p.shifter.io:20763', 'https': 'http://hades.p.shifter.io:20763'}, {'http': 'http://hades.p.shifter.io:20764', 'https': 'http://hades.p.shifter.io:20764'}, {'http': 'http://hades.p.shifter.io:20765', 'https': 'http://hades.p.shifter.io:20765'}, {'http': 'http://hades.p.shifter.io:20766', 'https': 'http://hades.p.shifter.io:20766'}, {'http': 'http://hades.p.shifter.io:20767', 'https': 'http://hades.p.shifter.io:20767'}, {'http': 'http://hades.p.shifter.io:20768', 'https': 'http://hades.p.shifter.io:20768'}, {'http': 'http://hades.p.shifter.io:20769', 'https': 'http://hades.p.shifter.io:20769'}, {'http': 'http://hades.p.shifter.io:20770', 'https': 'http://hades.p.shifter.io:20770'}, {'http': 'http://hades.p.shifter.io:20771', 'https': 'http://hades.p.shifter.io:20771'}, {'http': 'http://hades.p.shifter.io:20772', 'https': 'http://hades.p.shifter.io:20772'}, {'http': 'http://hades.p.shifter.io:20773', 'https': 'http://hades.p.shifter.io:20773'}, {'http': 'http://hades.p.shifter.io:20774', 'https': 'http://hades.p.shifter.io:20774'}, {'http': 'http://hades.p.shifter.io:20775', 'https': 'http://hades.p.shifter.io:20775'}, {'http': 'http://hades.p.shifter.io:20776', 'https': 'http://hades.p.shifter.io:20776'}, {'http': 'http://hades.p.shifter.io:20777', 'https': 'http://hades.p.shifter.io:20777'}, {'http': 'http://hades.p.shifter.io:20778', 'https': 'http://hades.p.shifter.io:20778'}, {'http': 'http://hades.p.shifter.io:20779', 'https': 'http://hades.p.shifter.io:20779'}, {'http': 'http://hades.p.shifter.io:20780', 'https': 'http://hades.p.shifter.io:20780'}, {'http': 'http://hades.p.shifter.io:20781', 'https': 'http://hades.p.shifter.io:20781'}, {'http': 'http://hades.p.shifter.io:20782', 'https': 'http://hades.p.shifter.io:20782'}, {'http': 'http://hades.p.shifter.io:20783', 'https': 'http://hades.p.shifter.io:20783'}, {'http': 'http://hades.p.shifter.io:20784', 'https': 'http://hades.p.shifter.io:20784'}, {'http': 'http://hades.p.shifter.io:20785', 'https': 'http://hades.p.shifter.io:20785'}, {'http': 'http://hades.p.shifter.io:20786', 'https': 'http://hades.p.shifter.io:20786'}, {'http': 'http://hades.p.shifter.io:20787', 'https': 'http://hades.p.shifter.io:20787'}, {'http': 'http://hades.p.shifter.io:20788', 'https': 'http://hades.p.shifter.io:20788'}, {'http': 'http://hades.p.shifter.io:20789', 'https': 'http://hades.p.shifter.io:20789'}, {'http': 'http://hades.p.shifter.io:20790', 'https': 'http://hades.p.shifter.io:20790'}, {'http': 'http://hades.p.shifter.io:20791', 'https': 'http://hades.p.shifter.io:20791'}, {'http': 'http://hades.p.shifter.io:20792', 'https': 'http://hades.p.shifter.io:20792'}, {'http': 'http://hades.p.shifter.io:20793', 'https': 'http://hades.p.shifter.io:20793'}, {'http': 'http://hades.p.shifter.io:20794', 'https': 'http://hades.p.shifter.io:20794'}, {'http': 'http://hades.p.shifter.io:20795', 'https': 'http://hades.p.shifter.io:20795'}, {'http': 'http://hades.p.shifter.io:20796', 'https': 'http://hades.p.shifter.io:20796'}, {'http': 'http://hades.p.shifter.io:20797', 'https': 'http://hades.p.shifter.io:20797'}, {'http': 'http://hades.p.shifter.io:20798', 'https': 'http://hades.p.shifter.io:20798'}, {'http': 'http://hades.p.shifter.io:20799', 'https': 'http://hades.p.shifter.io:20799'}, {'http': 'http://hades.p.shifter.io:20800', 'https': 'http://hades.p.shifter.io:20800'}, {'http': 'http://hades.p.shifter.io:20801', 'https': 'http://hades.p.shifter.io:20801'}, {'http': 'http://hades.p.shifter.io:20802', 'https': 'http://hades.p.shifter.io:20802'}, {'http': 'http://hades.p.shifter.io:20803', 'https': 'http://hades.p.shifter.io:20803'}, {'http': 'http://hades.p.shifter.io:20804', 'https': 'http://hades.p.shifter.io:20804'}, {'http': 'http://hades.p.shifter.io:20805', 'https': 'http://hades.p.shifter.io:20805'}, {'http': 'http://hades.p.shifter.io:20806', 'https': 'http://hades.p.shifter.io:20806'}, {'http': 'http://hades.p.shifter.io:20807', 'https': 'http://hades.p.shifter.io:20807'}, {'http': 'http://hades.p.shifter.io:20808', 'https': 'http://hades.p.shifter.io:20808'}, {'http': 'http://hades.p.shifter.io:20809', 'https': 'http://hades.p.shifter.io:20809'}, {'http': 'http://hades.p.shifter.io:20810', 'https': 'http://hades.p.shifter.io:20810'}, {'http': 'http://hades.p.shifter.io:20811', 'https': 'http://hades.p.shifter.io:20811'}, {'http': 'http://hades.p.shifter.io:20812', 'https': 'http://hades.p.shifter.io:20812'}, {'http': 'http://hades.p.shifter.io:20813', 'https': 'http://hades.p.shifter.io:20813'}, {'http': 'http://hades.p.shifter.io:20814', 'https': 'http://hades.p.shifter.io:20814'}, {'http': 'http://hades.p.shifter.io:20815', 'https': 'http://hades.p.shifter.io:20815'}, {'http': 'http://hades.p.shifter.io:20816', 'https': 'http://hades.p.shifter.io:20816'}, {'http': 'http://hades.p.shifter.io:20817', 'https': 'http://hades.p.shifter.io:20817'}, {'http': 'http://hades.p.shifter.io:20818', 'https': 'http://hades.p.shifter.io:20818'}, {'http': 'http://hades.p.shifter.io:20819', 'https': 'http://hades.p.shifter.io:20819'}, {'http': 'http://hades.p.shifter.io:20820', 'https': 'http://hades.p.shifter.io:20820'}, {'http': 'http://hades.p.shifter.io:20821', 'https': 'http://hades.p.shifter.io:20821'}, {'http': 'http://hades.p.shifter.io:20822', 'https': 'http://hades.p.shifter.io:20822'}, {'http': 'http://hades.p.shifter.io:20823', 'https': 'http://hades.p.shifter.io:20823'}, {'http': 'http://hades.p.shifter.io:20824', 'https': 'http://hades.p.shifter.io:20824'}, {'http': 'http://hades.p.shifter.io:20825', 'https': 'http://hades.p.shifter.io:20825'}, {'http': 'http://hades.p.shifter.io:20826', 'https': 'http://hades.p.shifter.io:20826'}, {'http': 'http://hades.p.shifter.io:20827', 'https': 'http://hades.p.shifter.io:20827'}, {'http': 'http://hades.p.shifter.io:20828', 'https': 'http://hades.p.shifter.io:20828'}, {'http': 'http://hades.p.shifter.io:20829', 'https': 'http://hades.p.shifter.io:20829'}, {'http': 'http://hades.p.shifter.io:20830', 'https': 'http://hades.p.shifter.io:20830'}, {'http': 'http://hades.p.shifter.io:20831', 'https': 'http://hades.p.shifter.io:20831'}, {'http': 'http://hades.p.shifter.io:20832', 'https': 'http://hades.p.shifter.io:20832'}, {'http': 'http://hades.p.shifter.io:20833', 'https': 'http://hades.p.shifter.io:20833'}, {'http': 'http://hades.p.shifter.io:20834', 'https': 'http://hades.p.shifter.io:20834'}, {'http': 'http://hades.p.shifter.io:20835', 'https': 'http://hades.p.shifter.io:20835'}, {'http': 'http://hades.p.shifter.io:20836', 'https': 'http://hades.p.shifter.io:20836'}, {'http': 'http://hades.p.shifter.io:20837', 'https': 'http://hades.p.shifter.io:20837'}, {'http': 'http://hades.p.shifter.io:20838', 'https': 'http://hades.p.shifter.io:20838'}, {'http': 'http://hades.p.shifter.io:20839', 'https': 'http://hades.p.shifter.io:20839'}]

url = "https://main.m.taobao.com/"
proxies = {"http": "http://hades.p.shifter.io:20759","https": "http://hades.p.shifter.io:20759"}
# proxies = None
# proxies = {"https":"http://127.0.0.1:8888"}

import logging
logging.basicConfig(level=logging.DEBUG, format="%(message)s")
logger = logging.getLogger()
def random_prox():
    return random.choice(Proxies_list)

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
        'user-agent': Random_UA(),
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
            # session.get(url, headers=headers, proxies=proxies, timeout=30)
            # session.get(url, headers=headers, proxies=random_prox(), timeout=30)
            session.get(url, headers=headers, proxies=abuyun_proxy(), timeout=30)
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
        'user-agent': Random_UA(),
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
            # session.get(url, headers=headers, proxies=proxies, timeout=30)
            # session.get(url, headers=headers, proxies=random_prox(), timeout=30)
            session.get(url, headers=headers, proxies=abuyun_proxy(), timeout=30)
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
        'user-agent': Random_UA(),
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
            # resp = session.get(url, headers=headers, proxies=proxies, verify=False, cookies=cookies, timeout=40)
            # resp = session.get(url, headers=headers, proxies=random_prox(), verify=False, cookies=cookies, timeout=40)
            resp = session.get(url, headers=headers, proxies=abuyun_proxy(), verify=False, cookies=cookies, timeout=40)
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
        'user-agent': Random_UA(),
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
    # resp = session.get(url, headers=headers, proxies=proxies, verify=False, cookies=cookies)
    # resp = session.get(url, headers=headers, proxies=random_prox(), verify=False, cookies=cookies)
    resp = session.get(url, headers=headers, proxies=abuyun_proxy(), verify=False, cookies=cookies)
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

        with open('content55.txt', 'a+') as f:
            f.write(da.encode('utf-8')+'\n')

    if repeat:
        raise Exception("repeat")
    return data,itemids

seed = {"keyword":""}
def get_page(page,prefix,itemsids="",cook=""):
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

    items,itemids = get(data, cookies=cook)

    return itemids


def runspider():
    cookies = gen_cookie()
    print cookies
    items = []
    for i in range(1,201):
        for j in range(200):
            try:
                get_page(i, "dddsda",",".join(items),cookies)
                # time.sleep(3)
                break
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                continue
        # time.sleep(3)
    print(len(allitemsdep))
runspider()
# 2190,2000
# 2010,2004
# 2000，2000

