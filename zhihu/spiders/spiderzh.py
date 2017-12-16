# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request

from zhihu.items import UserItem


class SpiderzhSpider(scrapy.Spider):
    name = 'spiderzh'
    allowed_domains = ['www.zhihu.com']

    #初始用户
    first_user = 'javabody'

    #用户信息
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include=locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,included_answers_count,included_articles_count,included_text,message_thread_token,account_status,is_active,is_bind_phone,is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,is_org_createpin_white_user,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'

    #关注者列表
    follow_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?offset={offset}&limit={limit}&include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    #粉丝列表
    fans_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?offset={offset}&limit={limit}&include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        yield Request(url = self.user_url.format(user = self.first_user), callback = self.parse_user)
        yield Request(url = self.follow_url.format(user = self.first_user, offset = 0, limit = 20), callback = self.parse_follow)
        yield Request(url = self.fans_url.format(user = self.first_user, offset = 0, limit = 20), callback = self.parse_fans)


    #解析用户
    def parse_user(self, response):
        json_data = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in json_data.keys():
                item[field] = json_data[field]

        if 'url_token' in json_data.keys():
            item['home_page'] = 'https://www.zhihu.com/people/%s' % (item['url_token'])
        #居住地
        if 'locations' in json_data.keys():
            item['locations'] = []
            for local in json_data['locations'] :
                item['locations'].append(local['name'])

        if 'business' in json_data.keys():
            item['business'] = json_data['business']['name']

        #教育经历
        if 'educations' in json_data.keys():
            item['educations'] = []
            for education in json_data['educations']:
                if 'school' in education.keys():
                    if 'major' in education.keys():
                        msg = education['school']['name'] + '/' + education['major']['name']
                    else:
                        msg = education['school']['name']
                else:
                    msg = education['major']['name']
                item['educations'].append(msg)
        #职业经历
        if 'employments' in json_data.keys():
            item['employments'] = []
            for employment in json_data['employments']:
                if 'company' in employment.keys():
                    if 'job' in employment.keys():
                        msg = employment['company']['name'] + '/' + employment['job']['name']
                    else:
                        msg = employment['company']['name']
                else:
                    msg = employment['job']['name']
                item['employments'].append(msg)

        yield item

        yield Request(url=self.follow_url.format(user = json_data.get('url_token'), offset = 0, limit = 20), callback = self.parse_follow)
        yield Request(url=self.fans_url.format(user = json_data.get('url_token'), offset = 0, limit = 20), callback = self.parse_fans)


    #解析关注者
    def parse_follow(self, response):
        json_data = json.loads(response.text)

        if 'data' in json_data.keys():
            for user in json_data.get('data'):
                yield Request(url = self.user_url.format(user = user.get('url_token')), callback = self.parse_user)

        if 'paging' in json_data.keys() and not json_data.get('paging').get('is_end'):
            next = json_data.get('paging').get('next')
            yield Request(url = next, callback = self.parse_follow)

    #解析粉丝
    def parse_fans(self, response):
        json_data = json.loads(response.text)
        if 'data' in json_data.keys():
            for user in json_data.get('data'):
                yield Request(url = self.user_url.format(user = user.get('url_token')), callback = self.parse_user)

        if 'paging' in json_data.keys() and not json_data.get('paging').get('is_end'):
            next = json_data.get('paging').get('next')
            yield Request(url = next, callback = self.parse_fans)




