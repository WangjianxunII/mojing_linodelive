# coding=utf-8
import sys

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

import socket

socket.setdefaulttimeout(10)
import random
import gzip
from StringIO import StringIO

import requests
import json
import urllib
import time
from pymongo import MongoClient
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
sign_s = requests.Session()
sign_s.headers.update({'Connection': 'Close'})


def safe(x):
    return x.encode('utf-8') if type(x) == unicode else x


chs = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

SIGN_HOST1 = '18.216.112.157:24318'
m_host = '192.168.198.173'
m_db = 'ali'

ttid = '1529386686433@lazada_android_6.75.1'


def get_app_login_message():
    client = MongoClient(host=m_host, port=27017)
    mongo_db = client[m_db]
    mongo_col_tbappcookie = mongo_db["tbappcookie"]
    res = mongo_col_tbappcookie.aggregate([
        {"$match": {"login_status": 1}},
        {"$sample": {"size": 1}},
    ])
    for login_cookie in res:
        uid = login_cookie['hid']
        sid = login_cookie['sid']
        data = login_cookie['data']
        data = json.loads(data)
        cookies = {}
        for cookie in data['cookies']:
            key_value = cookie.split(";", 1)[0]
            key = key_value.split("=", 1)[0]
            value = key_value.split("=", 1)[1]
            cookies[key] = value
        cookies_str = ""
        for key, value in cookies.items():
            cookies_str += key + "=" + value + ";"
        return sid, uid, cookies_str.strip(";")


def generate_did():
    return '%s' % ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') for i in range(24))


def generate_utdid():
    chs = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    return ''.join(random.choice(chs) for i in range(24))


def get_data_and_header(api, inputdata, v, pageId='', pageName='', extra_params={}, sid=None, uid=None, need_wua=False):
    t0 = str(int(time.time()))
    appkey = "23867946"
    device = {
        'ts': t0,
        'ttid': ttid,
        'did': generate_did(),
        #'did':'jDxrbIUwp1biREsNesz2vT2H',
        'did2': '%s' % ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') for i in range(44)),
        #'did2':'JZVJFPqNTQ0fj8EccG5VXVEZ3EeHAKkwrgbEqFVXOIox',
        'traceid': ''.join(random.choice(chs) for i in range(46)),
    }

    device.update(extra_params)
    inputdata = inputdata.replace(" ", "")
    data = {
        'uid': uid,
        'ttid': device['ttid'],
        'sid': sid,
        'x-features': '27',
        'data': inputdata,
        'v': v,
        'utdid': device['did'],
        't': device['ts'],
        'api': api,
        #'extdata': 'openappkey=DEFAULT_AUTH',
        'deviceId': device['did2'],
        'appKey': appkey
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "x-region-channel": "CN",
        "x-nettype": "WIFI",
        "x-nq": "WIFI",
        "A-SLIDER-Q": "appKey%3D21646297%26ver%3D1573617124712",
        "x-pv": "6.3",
        "cache-control": "no-cache",
        "x-c-traceid": device['traceid'],
        "x-appkey": appkey,
        "x-t": device['ts'],
        "x-page-name": pageName,
        "x-features": "27",
        "x-app-conf-v": "19",
        "a-orange-dq": "appKey=21646297&appVersion=9.16.0&clientAppIndexVersion=1120201121142600510",
        "x-utdid": device['did'],
        "user-agent": "MTOPSDK%2F3.1.1.7+%28Android%3B8.1.0%3BLenovo%3BLenovo+L58041%29",
        # "x-location":"%(lng)s%%2C%(lat)s" % device,
        "x-devid":  device['did2'],
        "x-bx-version": "6.5.23",
        "x-sgext": "923",
        "x-app-ver": "9.16.0",
        #"x-extdata": "openappkey%3DDEFAULT_AUTH",
        "x-ttid": urllib.quote(device['ttid']),
        "x-page-url": urllib.quote_plus(pageId),
        #"f-refer": "mtop"
    }
    head = {
        'x-features': '27',
        'x-sgext': '923',
        'x-page-name': pageName,
        'user-agent': 'MTOPSDK%2F3.1.1.7+%28Android%3B8.1.0%3BLenovo%3BLenovo+L58041%29',
        'x-ttid':  urllib.quote(device['ttid']),
        'cache-control': 'no-cache',
        'x-region-channel': 'CN',
        'x-appkey': appkey,
        "x-nettype": "WIFI",
        "x-nq": "WIFI",
        'x-c-traceid': device['traceid'],
        'x-app-conf-v': '19',
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'A-SLIDER-Q': 'appKey%3D21646297%26ver%3D1573617124712',
        'x-bx-version': '6.5.24',
        'x-pv': '6.3',
        'x-t':  device['ts'],
        'x-app-ver': '9.16.0',
        'f-refer': 'mtop',
        # 'x-social-attr': '2',
        'x-utdid': device['did'],
        'a-orange-dq': 'appKey=21646297&appVersion=9.16.0&clientAppIndexVersion=1120201121142600510',
        'x-devid': device['did2'],
        'x-page-url':  urllib.quote_plus(pageId),
    }
    if sid is not None and uid is not None:
        headers["x-sid"] = sid
        headers["x-uid"] = uid

    data2 = {'pageName': pageName, 'pageId': pageId}
    dataall = {'data1': json.dumps(data).replace(" ", ""), 'data2': json.dumps(data2).replace(" ", ""), 'b': need_wua}

    # for i in range(10):
    while True:
        try:
            postdata = json.dumps(dataall)
            # print len(postdata)
            postf = StringIO()
            gf = gzip.GzipFile(fileobj=postf, mode='wb')
            gf.write(postdata)
            gf.close()
            postdata = postf.getvalue()

            r = requests.post('https://%s/sign' % SIGN_HOST1, postdata, timeout=1200, verify=False)
            if r.status_code != 200 or r.content == 'timeout' or r.content == 'error' or r.content.startswith('Traceback'):
                print 'aaaa', r.content
                time.sleep(10)
                continue

            rx = json.loads(r.content)
            if isinstance(rx, unicode):
                rx = json.loads(rx)
            if 'x-sign' in rx and 'x-mini-wua' in rx:
                break
                # print "rx=>", rx
            time.sleep(5)
        except KeyboardInterrupt:
            exit(1)
        except Exception, e:
            print "e=>", e
            # import traceback
            # print traceback.format_exc()
            # break
            time.sleep(5)
            pass

    headers['x-sign'] = urllib.quote(rx['x-sign'])
    headers['x-mini-wua'] = urllib.quote(rx['x-mini-wua'])
    headers['x-sgext'] = urllib.quote(rx['x-sgext'])
    headers['x-umt'] = urllib.quote(rx['x-umt'])
    if need_wua:
        try:
            data['wua'] = urllib.quote(rx['wua'])
        except:
            data['wua'] = ""
    return data, headers


if __name__ == '__main__':

    import sys
    import time
    import random

    # proxy = sys.argv[1]
    # p = {'http': 'http://%s' % proxy, 'https': 'http://%s' % proxy}
    #
    proxies = []
    for i in range(5488, 5588):
        proxies.append({'http': 'http://163.172.110.216:%d' % i, 'https': 'http://163.172.110.216:%d' % i})
        # proxies.append({'http': 'http://mojing:Mojing2019@116.196.89.140:%d' % i, 'https': 'http://mojing:Mojing2019@116.196.89.140:%d' % i})

    # p = {'http': 'http://v.yhtip.com:1030', 'https': 'http://v.yhtip.com:1030'}
    # p = {}

    s = requests.session()
    # 获取登录信息
    # sid, uid, cookie_str = get_app_login_message()
    # sid = "16a2dbc1ee7530e72b515b2be653fee5"
    # uid = "2211065991133"
    cookie_str = ""
    sid = uid = None
    for i in range(10):
        utdid = generate_utdid()
        t0 = int(time.time())
        api = "mtop.lazada.gsearch.appsearch"
        data = {
            "__original_url__": "http%3A%2F%2Fwww.lazada.com.my%2Fshop-headphones-headsets%2F%3Fpos%3D1%26acm%3D201711220.1003.1.2873589%26scm%3D1003.1.201711220.OTHER_154_2873589%26from%3Dlp_category%26searchFlag%3D1%26",
            "acm": "201711220.1003.1.2873589", "adjustID": "", "deviceID": "203d9ef11b4f3d82|849df9e2-0715-4ba0-9cf2-79375bfda760", "firstSearch": "true", "from": "lp_category",
            "latitude": "0.0", "longitude": "0.0", "n": "10", "page": "1", "pos": "1", "rainbow": "143,2,122,131", "scm": "1003.1.201711220.OTHER_154_2873589", "searchFlag": "1",
            "speed": "15.9", "sversion": "5.0", "ttid": "1529386686433@lazada_android_6.75.1", "url_key": "shop-headphones-headsets/", "userID": "",
            "utd_id": "X7xmHufwTpEDAPmYDVelKKdP", "vm": "nw"}

        v = "1.0"
        ex_params = {'did': "X7xmHufwTpEDAPmYDVelKKdP",
                     "did2": "203d9ef11b4f3d82|849df9e2-0715-4ba0-9cf2-79375bfda760"}
        # did = utdid
        # did2 = deviceId
        need_wua = False
        data, headers = get_data_and_header(api, json.dumps(data), v, extra_params=ex_params, sid=sid, uid=uid, need_wua=need_wua)
        print time.time() - t0
        if cookie_str != "":
            headers['cookie'] = cookie_str
        # break
        url = 'https://acs-m.lazada.com.my/gw/%s/%s/' % (api, v)
        params = {
            "data": data['data'],
        }
        if need_wua:
            params['wua'] = data["wua"]
        url += "?" + urllib.urlencode(params)

        # postdata = urllib.urlencode({'data': data['data']})
        # print url, headers
        # p = random.choice(proxies)
        # p = {}
        r = s.get(url, headers=headers, verify=False, proxies=None)
        print r.headers
        print r.url
        print r.content

        # break