#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 10:21:32 2021

@author: wolf
"""
import sys
import os
import random
import requests
import codecs
import base64
import datetime
import re
import time

user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
    "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

user_agent = random.choice(user_agent_list)
headers = {'Accept': '*/*',
           'Accept-Language': 'en-US,en;q=0.8',
           'Cache-Control': 'max-age=0',
           # 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
           'Connection': 'keep-alive'}

def get_file(url, targetfile):
    """
    ???url??????????????????????????????
    """
    global headers
    try:
        req = requests.get(url, headers=headers) # ??????????????????
        with open(targetfile, "wb") as code:
            code.write(req.content)
            print("====>>>Successfully saving %s" %targetfile)

        return True
    except:
        print('??????????????????')
        return False

# ?????????????????????????????????
root_dir = os.path.dirname(os.path.abspath(__file__))#os.path.split(__file__)[0]
print('??????????????????', root_dir)
# print()

for file0 in os.listdir(root_dir):
    # ??????????????????
    file_path = os.path.join(root_dir, file0)
    print('checking:', file_path)

    # ???????????????
    if not os.path.isfile(file_path):
        continue
    # ?????????md??????
    if not os.path.splitext(file0)[-1] == '.md':
        continue

    with codecs.open(file_path, 'r', 'utf-8') as fp:
        text = fp.read()

    # ????????????http?????????url
    comp = re.compile(r"(?<=\!\[img\]\()http.+?(?=\))", re.S)

    img_url_l = comp.findall(text)

    # ????????????url
    for img_url0 in img_url_l:

        # ?????????????????????
        target_name = re.sub(r'http.+/', '', img_url0)

        # ??????????????????????????????
        if len(target_name) < 10:
            target_name = str(int(time.time())) + target_name

        target_path = './img/' + target_name

        # ????????????????????????????????????????????????
        while os.path.exists(target_path):
            target_name = str(random.randint(0,9)) + target_name
            target_path = './img/' + target_name

        # ????????????
        resp = get_file(img_url0, os.path.abspath(target_path))

        # ?????????????????????md?????????????????????????????????????????????????????????log??????
        if resp:
            text = text.replace(img_url0, target_path)
            with codecs.open(file_path, 'w', 'utf-8') as fp:
                fp.write(text)
        else:
            with codecs.open(os.path.join(root_dir, 'download.log'), 'a', 'utf-8') as fp:
                fp.write('???????????????' + img_url0 + '\n')
