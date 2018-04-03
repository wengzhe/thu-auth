#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'WZ'

import yaml
import requests
import hashlib
import re
import time
import json
import math
import urllib.parse
import hmac

login_url = {
            'IPv4': "https://auth4.tsinghua.edu.cn",
            # 'IPv6': "https://auth6.tsinghua.edu.cn"
            }
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1)" \
            " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36"


def check_sign_int32(i):
    i += 0x1000000000
    i &= 0xFFFFFFFF
    if i & 0x80000000:
        return i-0x100000000
    return i


def check_unsigned_int32(i):
    i += 0x1000000000
    i &= 0xFFFFFFFF
    return i


def xEncode(str, key):
    def s(a, b):
        c = len(a)
        v = []
        for i in range(0, (c//4)*4, 4):
            v.append(check_sign_int32(ord(a[i]) | ord(a[i + 1]) << 8 | ord(a[i + 2]) << 16 | ord(a[i + 3]) << 24))
        if (c//4)*4 < c:
            t = 0
            for j in range((c//4)*4, c):
                t |= ord(a[j]) << 8*(j-(c//4)*4)
            v.append(t)
        if b:
            v.append(c)
        return v

    def l(a, b):
        d = len(a)
        c = (d - 1) << 2
        if b:
            m = a[d - 1]
            if (m < c - 3) or (m > c):
                return None
            c = m
        for i in range(d):
            a[i] = check_unsigned_int32(a[i]).to_bytes(4, byteorder='little')
        if b:
            return b''.join(a)[0:c]
        else:
            return b''.join(a)

    if str == "":
        return ""

    v = s(str, True)
    k = s(key, False)
    if len(k) < 4:
        for i in range(len(k), 4):
            k.append(0)
    n = len(v) - 1
    z = v[n]
    y = v[0]
    c = check_sign_int32(0x86014019 | 0x183639A0)
    q = math.floor(6 + 52 / (n + 1))
    d = 0
    while 0 < q:
        q -= 1
        d = d + check_sign_int32(c & (0x8CE0D9BF | 0x731F2640))
        e = (d >> 2) & 3
        for p in range(n):
            y = v[p + 1]
            m = (check_unsigned_int32(z) >> 5) ^ check_sign_int32(y << 2)
            m += ((check_unsigned_int32(y) >> 3) ^ (z << 4)) ^ (d ^ y)
            m += k[(p & 3) ^ e] ^ z
            z = v[p] = check_sign_int32(v[p] + check_sign_int32(m & (0xEFB8D130 | 0x10472ECF)))
        y = v[0]
        m = (check_unsigned_int32(z) >> 5) ^ check_sign_int32(y << 2)
        m += (check_unsigned_int32(y) >> 3) ^ (z << 4) ^ (d ^ y)
        m += k[(n & 3) ^ e] ^ z
        z = v[n] = check_sign_int32(v[n] + check_sign_int32(m & (0xBB390742 | 0x44C6F8BD)))
    return l(v, False)


def current_milli_time():
    return int(round(time.time() * 1000))


def load_config(path="config/account.yaml"):
    with open(path) as f:
        config = yaml.load(f)
        username = config["account"]["username"]
        password = config["account"]["password"]

        return username, password


def get_data(url):
    pattern = re.compile(r'<input type="hidden" id="user_ip" name="user_ip" value="(.*?)">')
    return re.findall(pattern, requests.get(url+"/srun_portal_pc.php?ac_id=1&").text)


def base64(t):
    n = "LVoJPiCN2R8G90yg+hmFHuacZ1OWMnrsSTXkYpUq/3dlbfKwv6xztjI7DeBE45QA"
    r = "="
    u = ""
    a = len(t)
    for o in range(0, a, 3):
        h = int(t[o]) << 16 | (int(t[o + 1]) << 8 if o + 1 < a else 0) | (int(t[o + 2]) if o + 2 < a else 0)
        for i in range(4):
            if o * 8 + i * 6 > a * 8:
                u += r
            else:
                u += n[h >> 6 * (3 - i) & 63]
    return u


def get_token(url, username):
    callback = 'heiheihei_%d' % (current_milli_time())
    url += '/cgi-bin/get_challenge?callback=%s&username=%s&ip=&double_stack=1&_=%d'\
           % (callback, username, current_milli_time())
    pattern = re.compile(r'"challenge":"(.*?)"')
    return re.findall(pattern, requests.get(url).text), callback


def go_online(url, ip):
    username, password = load_config()
    token, callback = get_token(url, username)
    token = token[0]
    enc = 'srun_bx1'
    data = {
        "action": "login",
        "username": username,
        "password": password,
        "ac_id": "1",
        "double_stack":"1",
        "ip": "",
        "n": "200",
        "type": "1",
        "callback": callback,
        "_": current_milli_time(),
    }
    js_str = json.dumps({"username": data['username'], "password": data['password'], "ip": data['ip'], "acid": data['ac_id'], "enc_ver": enc}).replace('": "', '":"').replace(', "', ',"')
    data['info'] = ("{SRBX1}" + base64(xEncode(js_str, token)))
    hmd5 = hmac.new(token.encode(), b'', 'MD5').hexdigest()
    data['password'] = ("{MD5}" + hmd5)
    data['chksum'] = hashlib.sha1((token + data['username'] + token + hmd5 + token + data['ac_id'] + token + data['ip']
                                + token + data['n'] + token + data['type'] + token + data['info']).encode()).hexdigest()
    login_url_final = url+'/cgi-bin/srun_portal?callback=%s&action=login&username=%s&password=%s&ac_id=1&ip=&double_stack=1&info=%s&chksum=%s&n=200&type=1&_=%d'\
                      % (urllib.parse.quote(data['callback']), data['username'], urllib.parse.quote(data['password']), urllib.parse.quote(data['info']).replace('/', '%2F'), data['chksum'], data['_'])
    res = requests.get(login_url_final)

    return res.text


def check_online():
    for key in login_url:
        ip_addr = get_data(login_url[key])
        if len(ip_addr):
            print(key, 'is not online!')
            print(go_online(login_url[key], ip_addr[0]))
            return

    print('All Online!')
    return


def main():
    check_online()


if __name__ == "__main__":
    main()

