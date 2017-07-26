# -*- coding: utf-8 -*-


__Author__ = "Leng Fuping"
__Doc__ = "baidu wenku sign everyday."

from scrapy.spiders import Spider
from my_scrapy.items import DmozItem
import logging
import logging.config
from scrapy.http import Request
import time
import urllib
import re
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import base64
import math
import random



logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='baidu_wenku_signin_spider.log',
                filemode='a') #default 'a', if set 'w', the log file will be rewrite every runtime.

BAIDU_HOME_PAGE_URL = "https://www.baidu.com/"
BAIDU_GET_TOKEN_URL = 'https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&class=login&logintype=basicLogin'
BAIDU_GET_LOGIN_HISTORY_URL = 'https://passport.baidu.com/v2/api/?loginhistory&tpl=pp&apiver=v3'
BAIDU_LOGIN_CHECK_URL = 'https://passport.baidu.com/v2/api/?logincheck&tpl=pp&apiver=v3&sub_source=leadsetpwd&username=18600890116&isphone=false&callback=bd__cbs__u1vvyu'
BAIDU_GET_PUBLIC_KEY_URL = 'https://passport.baidu.com/v2/getpublickey?tpl=pp&apiver=v3'
BAIDU_LOGIN_URL = "https://passport.baidu.com/v2/api/?login"
BAIDU_WENKU_SIGNIN_URL = "http://wenku.baidu.com/task/submit/signin"

COMMON_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Connection": "keep-alive",
    "Cache-Control": "Cache-Control",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
    "Pragma":"no-cache"
}

class BaiduWenkuSigninSpider(Spider):
    name="baidu_wenku_signin"
    start_urls = ['https://www.yinxiang.com/']

    def parse(self, response):
        DmozItem['content'] = self.get_home_page().body
        yield self.get_home_page()

    def get_callback_method_name(self):
        method_name_str = 'bd__cbs__' + str(math.floor(2147483648 * random.random()))
        logging.info("get callback method name is %s",method_name_str)
        return method_name_str

    def get_gid(self):
        return 'F970A89-DB7D-4F4B-B1CF-8CE2AA219D49'

    def get_home_page(self):
        COMMON_HEADERS["Host"] = "www.baidu.com"
        request = Request(BAIDU_HOME_PAGE_URL, headers=COMMON_HEADERS,callback=self.parse_get_home_page_result)
        return request

    def parse_get_home_page_result(self, response):
        if response.status is 200:
            logging.info("get baidu home page success!")
            yield self.get_token()
        else:
            logging.error("get baidu home page failed, the httpstatus is: %s", response.status)

    def get_token(self):
        COMMON_HEADERS["Host"] = "passport.baidu.com"
        full_baidu_get_token_url = BAIDU_GET_TOKEN_URL+"&tt="+'%d' % (time.time() * 1000)+"&callback="+self.get_callback_method_name()+"&gid="+self.get_gid()
        request = Request(full_baidu_get_token_url, headers=COMMON_HEADERS, callback=self.parse_get_token_result)
        return request

    def parse_get_token_result(self,response):
        if response.status is 200:
            reg_token = re.compile("\"token\"\s+:\s+\"(\w+)\"")
            self._token = reg_token.findall(str(response.body))[0]
            logging.info("get token success! the token is: %s",self._token)
            yield self.login_history()
        else:
            logging.error("get baidu login token failed, the httpstatus is: %s", response.status)

    def login_history(self):
        COMMON_HEADERS["Host"] = "passport.baidu.com"
        COMMON_HEADERS["Referer"] = "https://passport.baidu.com/v2/?login&u=http://wenku.baidu.com/task/browse/daily"
        COMMON_HEADERS["Accept"] = "*/*"
        COMMON_HEADERS["Cache-Control"] = "no-cache"
        full_baidu_get_login_history_url = BAIDU_GET_LOGIN_HISTORY_URL+"&token="+self._token+"&tt="+'%d' % (time.time() * 1000)+"&callback="+self.get_callback_method_name()+"&gid="+self.get_gid()
        request = Request(full_baidu_get_login_history_url, headers=COMMON_HEADERS, callback=self.parse_login_history_result)
        return request

    def parse_login_history_result(self,response):
        if response.status is 200:
            logging.info("get login history response is: %s",response.body)
            yield self.login_check()
        else:
            logging.error("get baidu login token failed, the httpstatus is: %s", response.status)

    def login_check(self):
        full_baidu_login_check_url = BAIDU_LOGIN_CHECK_URL + "&token=" + self._token+"&tt="+'%d' % (time.time() * 1000)+"&callback="+self.get_callback_method_name()+"&gid="+self.get_gid()
        request = Request(full_baidu_login_check_url, headers=COMMON_HEADERS,
                          callback=self.parse_login_check_result)
        return request

    def parse_login_check_result(self,response):
        if response.status is 200:
            logging.info("get login check response is: %s",response.body)
            yield self.getpublickey()
        else:
            logging.error("get baidu login check failed, the httpstatus is: %s", response.status)

    def getpublickey(self):
        full_get_public_key_url = BAIDU_GET_PUBLIC_KEY_URL + "&token=" + self._token+"&tt="+'%d' % (time.time() * 1000)+"&callback="+self.get_callback_method_name()+"&gid="+self.get_gid()
        request = Request(full_get_public_key_url, headers=COMMON_HEADERS,
                          callback=self.parse_get_public_key_result)
        return request

    def parse_get_public_key_result(self, response):
        if response.status is 200:
            logging.info("get public key response is: %s", response.body)
            rsa_key_pattern = re.compile("\"key\"\s*:\s*'(\w+)'")
            match = rsa_key_pattern.search(response.text)
            if match:
                rsa_key = match.group(1)
                self._pwd_rsa_key = rsa_key
                logging.info("rsa_key is %s",rsa_key)
            else:
                logging.error("get rsa_key failed!")

            rsa_public_key_pattern = re.compile("\"pubkey\":'(.+?)'")
            match = rsa_public_key_pattern.search(response.text)
            if match:
                rsa_public_key = match.group(1)
                rsa_public_key = rsa_public_key.replace('\\n', '\n').replace('\\', '')
                self._pwd_public_rsa_key = rsa_public_key
                logging.info("rsa_public_key is %s", rsa_public_key)
            else:
                logging.error("get rsa_public_key failed!")
            yield self.login().next()
        else:
            logging.error("get  public key failed, the httpstatus is: %s", response.status)

    def login(self):
        COMMON_HEADERS["Host"] = "passport.baidu.com"
        COMMON_HEADERS["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        COMMON_HEADERS["Cache-Control"] = "no-cache"
        COMMON_HEADERS["Accept-Encoding"] = "gzip, deflate, br"
        COMMON_HEADERS["Origin"] = "https://passport.baidu.com"
        COMMON_HEADERS["Upgrade-Insecure-Requests"] = 1

        bdData = {
            "staticpage": "https://passport.baidu.com/static/passpc-account/html/v3Jump.html",
            "charset" : "UTF-8",
            "token": self._token,
            "tpl": "pp",  # 重要,需要跟TOKEN_URL中的相同
            "apiver" : "v3",
            "u" : "http://wenku.baidu.com/task/browse/daily",
            "isPhone" : "",
            "safeflg":"0",
            "detect":"1",
            "quick_user":"0",
            "loginmerge":"true",
            "mem_pass":"on",
            "crypttype":"12",
            "logintype" : "basicLogin",
            "logLoginType" : "pc_loginBasic",
            "username": "",
            "password": "",
            "rsakey" : self._pwd_rsa_key,
            "tt": '%d' % (time.time() * 1000),
            'ppui_logintime': 71755,
            'gid': self.get_gid(),
            "codeString":"",
            "verifycode":""
        }
        #必须要加上，否则报错：err_no=257(请输入验证码)
        cookies = [{'name': 'FP_UID', 'value': 'a8e078358d61a058b43420dee15e9e77', 'domain': 'baidu.com','path': '/'}]

        #get_user_and_pwd
        for line in open("baidu_wenku_user.conf"):
            user, password = str(line).strip('\n').split(",")
            bdData["username"] = user

            rsakey = RSA.importKey(self._pwd_public_rsa_key)
            cipher = PKCS1_v1_5.new(rsakey)
            password = base64.b64encode(cipher.encrypt(password))
            logging.info("after encrypt, the pwd is %s",password)

            bdData["password"] = password
            postData = urllib.urlencode(bdData).encode("utf-8")
            logging.info("login post data is: %s",postData)
            yield Request(BAIDU_LOGIN_URL, headers=COMMON_HEADERS, cookies=cookies, body=postData, method="POST",callback=self.parse_login_result)

    def parse_login_result(self,response):
        if response.status is 200:
            logging.info("login response is : %s", response.body)
            if response.body.find("err_no=0") > -1:
                logging.info("login baidu success!")
            else:
                logging.error("login baidu failed")
        else:
            logging.error("post baidu login failed, the httpstatus is: %s", response.status)