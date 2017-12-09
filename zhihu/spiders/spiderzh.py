# -*- coding: utf-8 -*-
import scrapy


class SpiderzhSpider(scrapy.Spider):
    name = 'spiderzh'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    def parse(self, response):
        print('**************************')
        print(response.text)
        print('**************************')
