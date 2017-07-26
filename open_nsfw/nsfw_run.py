#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    时间段批量处理不正规图片
    @auth <574747417@qq.com>
"""
import os
import re
import time

nsfw_img_path = []
# 设置时间段图片处理 单位:分钟 处理当前时间前多少分钟的图片
Time_interval_between = 120
# 设置图片等级进行处理,越高表示图片越不正规 等级为0.1-1.0
score_level = 0.9
for root, dirs, files in os.walk('/var/www/html/yysj/open_nsfw/img'):
    for filespath in files:
        path = os.path.join(root, filespath)
        if (int(os.path.getctime(path)) >= int((time.time() - Time_interval_between * 60))):
            result = os.popen(
                "python /var/www/html/yysj/open_nsfw/classify_nsfw.py  --model_def /var/www/html/yysj/open_nsfw/nsfw_model/deploy.prototxt --pretrained_model  /var/www/html/yysj/open_nsfw/nsfw_model/resnet_50_1by2_nsfw.caffemodel " + path)
            mode = re.compile(r'\d+.*')
            try:
                score = float(mode.findall(result.read())[0])
                if (score >= score_level):
                    os.remove(path)
                    nsfw_img_path.append(path)
            except IndexError:
                continue

print nsfw_img_path
