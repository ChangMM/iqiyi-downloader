#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os, re
import sys, time
import requests
import configparser
from tqdm import tqdm

CURRENTPATH = os.path.split(os.path.realpath(__file__))[0]
CACHEPATH = CURRENTPATH + os.sep + ".cache"
METAFILEPATH = CACHEPATH + os.sep + 'metafile'
TSPATH = CACHEPATH + os.sep + 'ts' + os.sep

config = configparser.RawConfigParser()
config.read('config.ini')
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Connection": "keep-alive",
    "Cookie": config.get("headers", "Cookie"),
    "Pragma": config.get("headers", "Pragma"),
    "Cache-Control": config.get("headers", "Cache-Control"),
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": config.get("headers", "User-Agent")
}

def mkdir(path):
    path = path.strip()
    path = path.rstrip(os.sep)

    if not os.path.exists(path):
        os.makedirs(path)

def init():
    mkdir()

def clear():
    # 删除 TS 文件夹中的文件
    for root, dirs, files in os.walk(TSPATH):
        for name in files:
            os.remove(os.path.join(root, name))

    # 清空 metafile 的文件
    f = open(METAFILEPATH,"w")
    f.truncate()

def formatUrl(url):
    # todo
    return url

def downloadTSFile():
    index = 0
    lastStop = int(config.get("download", "index"))
    total = 0
    # 获取需要下载的总的 ts 文件数
    for line in open(METAFILEPATH):
        if "http" in line:
            total = total + 1
    pbar = tqdm(desc = "下载进度：", total = total)

    for line in open(METAFILEPATH):
        if "http" in line:
            if index < lastStop:
                continue

            HEADERS["Host"] = "data.video.iqiyi.com"
            res1 = requests.get(line.strip('\n'), headers=HEADERS, allow_redirects=False)
            locationURL1 = res1.headers["Location"]

            matchObj = re.match(r'http://(.*?)/', locationURL1, re.M|re.I)
            HEADERS["Host"] = matchObj.group(1)
            res2 = requests.get(locationURL1, headers=HEADERS, allow_redirects=False)

            while("Location" not in res2.headers):
                time.sleep(1)
                HEADERS["Host"] = "data.video.iqiyi.com"
                res1 = requests.get(line, headers=HEADERS, allow_redirects=False)
                locationURL1 = res1.headers["Location"]
                matchObj = re.match( r'http://(.*?)/', locationURL1, re.M|re.I)
                HEADERS["Host"] = matchObj.group(1)
                res2 = requests.get(locationURL1, headers=HEADERS, allow_redirects=False)

            locationURL2 = res2.headers["Location"]

            matchObj2 = re.match( r'http://(.*?)/', locationURL2, re.M|re.I)
            HEADERS["Host"] = matchObj2.group(1)
            r = requests.get(locationURL2, headers=HEADERS)
            with open(TSPATH + str(index) + '.ts', 'wb') as fs:
                fs.write(r.content)
            pbar.update(1)
            index = index + 1
            config.set("download", "index", index)
            config.write(open('config.ini', 'w'))

def download(url):
    HEADERS["Host"] = "cache.m.iqiyi.com"
    with requests.get(formatUrl(url), headers=HEADERS, stream=True) as r:
        with open(METAFILEPATH, 'wb') as fs:
            fs.write(r.content)

if __name__ == "__main__":
    url = sys.argv[1] or ""
    if url is "":
        print("请输入链接")
    else:
        # clear()
        # download(url)
        downloadTSFile()
