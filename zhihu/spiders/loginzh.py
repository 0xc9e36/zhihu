# -*- coding: utf-8 -*-
import json
from PIL import Image
import scrapy
import time
from scrapy import Request, FormRequest

#模拟知乎登录
#下载验证码到本地，手动输入信息，发送请求

class LoginzhSpider(scrapy.Spider):
    name = 'loginzh'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://zhihu.com/']
    captcha_path = 'resource/captcha.gif'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'authorization': 'Bearer Mi4xQTRjV0FRQUFBQUFBVUVKU1ZZWE9EQmNBQUFCaEFsVk5Bd29aV3dENFU4UXVJX1JBMFBWUzYzLXVEb3VsT2hQYk53|1512815619|734f479b1d10af314b78e094e80739279fedd3b2',
    }

    def start_requests(self):
        timestamp = str(int(time.time()))
        type = 'login'
        lang = 'en'
        captcha_url = 'https://www.zhihu.com/captcha.gif?r=%s&type=%s&lang=%s' % (timestamp, type, lang)
        print(captcha_url)
        yield Request(url = captcha_url, headers = self.headers, callback = self.parse_captcha)

    #验证码解析
    def parse_captcha(self, response):
        with open(self.captcha_path, 'wb') as f:
            f.write(response.body)
            f.close()

        im = Image.open(self.captcha_path)
        im.show()
        im.close()
        captcha = input("input the captcha with quotation mark\n>")
        yield Request(url = 'https://www.zhihu.com/', callback = self.login, meta = {'captcha':captcha})


    def login(self, response):
        xsrf = response.xpath('/html/body/div[1]/div/div[2]/div[2]/form/input/@value').extract()[0]

        #只模拟了邮箱登录
        login_url = 'https://www.zhihu.com/login/email'
        yield FormRequest(url = login_url,
                          method = 'POST',
                          formdata = {
                              'captcha_type': 'en',
                              'email': '****',
                              'password':'****',
                              '_xsrf': xsrf,
                              'captcha_type': 'en',
                              'captcha': response.meta['captcha'],
                            },
                            callback = self.after_login,
                            )

    def after_login(self,response):
        json_data = json.loads(response.text)
        print(json_data)
        yield Request(url='https://www.zhihu.com/settings/account', callback=self.login_test)

    """
    登录测试
    在 settings.py 中设置COOKIES_ENABLED = True，即可在 Request 中共享 Cookie
    """
    def login_test(self, response):
        print(response.text)
