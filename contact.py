#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys

CURRENTPATH = os.path.split(os.path.realpath(__file__))[0]
CACHEPATH = CURRENTPATH + os.sep + ".cache"

dirs = CACHEPATH + os.sep + "ts"
mp4 = CACHEPATH + os.sep + "mp4"

# 删除之前的文件
for _, _, files in os.walk(mp4):
    for name in files:
        os.remove(os.path.join(root, name))

# 获取最后合并后的文件名称
filename = '~/Desktop/' + (sys.argv[1] or "自动合并名称") + ".mp4"

# 合并
a = 1
content = ""
lists = os.listdir(dirs)
lists = sorted(lists, key=lambda name: int(name.split('.')[0]))

b = [lists[i:i+250] for i in range(0,len(lists),250)]
for lis in b:
    cmd = "cd %s && ffmpeg -i \"concat:"%mp4
    for file in lis:
        if file != '.DS_Store':
            file_path = os.path.join(dirs, file)
            cmd += file_path + '|';
    cmd = cmd[:-1]
    cmd += '" -bsf:a aac_adtstoasc -c copy -vcodec copy %s.mp4'%a
    try:
        os.system(cmd)
        content += "file '%s.mp4'\n"%a
        a = a+1
    except:
        print("Unexpected error")

fp = open("%s/mp4list.txt"%mp4,'a+')
fp.write(content)
fp.close()
mp4cmd = "cd %s && ffmpeg -y -f concat -i mp4list.txt -c copy %s"%(mp4, filename)
os.system(mp4cmd)
