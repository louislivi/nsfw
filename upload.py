#coding=utf-8
"""
    子山<574747417@qq.com>
"""
import commands
import bottle
from bottle import route, run, template
@route('/alisa')
def index():
    params = bottle.request.params
    filename=params.get("filename", None)
    print filename
    command = "python /var/www/html/image.processing/open_nsfw/classify_nsfw.py  --model_def /var/www/html/image.processing/open_nsfw/nsfw_model/deploy.prototxt --pretrained_model  /var/www/html/image.processing/open_nsfw/nsfw_model/resnet_50_1by2_nsfw.caffemodel "+"/var/www/html/image.processing/upload/"+filename
    # output = os.popen(command)
    return template('<b>{{text}}</b>', text=commands.getoutput(command))
run(host='localhost', port=8888)