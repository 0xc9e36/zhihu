# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request

from zhihu.items import UserItem


class SpiderzhSpider(scrapy.Spider):
    name = 'spiderzh'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    #初始url
    first_user = 'jjmoe'

    #用户主页
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_include = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'

    #用户关注的人list
    follow_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follow_include = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    #粉丝list
    fans_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    fans_include = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        #yield Request(url = 'http://httpbin.org/get', callback = self.parse_user)
        yield Request(self.user_url.format(user = self.first_user, include = self.user_include), self.parse_user)
        yield Request(self.follow_url.format(user = self.first_user, include = self.follow_include, offset = 0, limit = 20), self.parse_follow)
        yield Request(self.fans_url.format(user = self.first_user, include = self.fans_include, offset = 0, limit = 20), self.parse_fans)

    #用户回调
    def parse_user(self, response):
        #print(response.text)
        json_data = json.loads(response.text)
        item = UserItem()

        for field in item.fields:
            if field in json_data.keys():
                item[field] = json_data.get(field)
        yield item

        yield Request(self.follow_url.format(user = json_data.get('url_token'), include = self.follow_include, offset = 0, limit = 20), self.parse_follow)
        yield Request(self.fans_url.format(user = json_data.get('url_token'), include = self.fans_include, offset = 0, limit = 20), self.parse_fans)


    #关注回调
    def parse_follow(self, response):
        json_data = json.loads(response.text)

        if 'data' in json_data.keys():
            for user in json_data.get('data'):
                yield Request(self.user_url.format(user=user.get('url_token'), include=self.user_include), self.parse_user)

        if 'paging' in json_data.keys() and not json_data.get('is_end'):
            next_url = json_data.get('paging').get('next')
            yield Request(next_url, self.parse_follow)

    #粉丝回调
    def parse_fans(self, response):
        json_data = json.loads(response.text)

        if 'data' in json_data.keys():
            for user in json_data.get('data'):
                yield Request(self.user_url.format(user=user.get('url_token'), include=self.user_include), self.parse_user)

        if 'paging' in json_data.keys() and not json_data.get('is_end'):
            next_url = json_data.get('paging').get('next')
            yield Request(next_url, self.parse_fans)
