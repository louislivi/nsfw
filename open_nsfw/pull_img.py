#-*- coding:utf-8 -*-
"""
    从百度下载图片
    @auth <574747417@qq.com>
"""
import re
import requests
import random
import time
import os
#需要下载多少页到多少页
page = [10,20]
score_level = 0.9
images = []
#i = 0
for pn in range(page[0],page[1]*10,10):
    print('开始下载page'+ str(int(pn)/10) +'页...')
    url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=%E7%BE%8E%E5%A5%B3&pn='+str(pn)+'&gsm=3c&ct=&ic=0&lm=-1&width=0&height=0'
    html = requests.get(url).text
    pic_url = re.findall('"objURL":"(.*?)",',html,re.S)
    for each in pic_url:
        try:
            pic= requests.get(each, timeout=10)
        except requests.exceptions.ConnectionError:
            print '【错误】当前图片无法下载'
            continue
        string = '/var/www/html/yysj/open_nsfw//img/'+str(time.time())+str(random.randrange(0, 100)) + '.jpg'
        fp = open(string,'wb')
        fp.write(pic.content)
        fp.close()
        result = os.popen(
            "python /var/www/html/yysj/open_nsfw/classify_nsfw.py  --model_def /var/www/html/yysj/open_nsfw/nsfw_model/deploy.prototxt --pretrained_model  /var/www/html/yysj/open_nsfw/nsfw_model/resnet_50_1by2_nsfw.caffemodel " + string)
        mode = re.compile(r'\d+.*')
        try:
            score = float(mode.findall(result.read())[0])
            if (score <= score_level):
                os.remove(string)
            else:
                images.append(string)
                print string
        except IndexError:
            continue
        #i += 1

print images