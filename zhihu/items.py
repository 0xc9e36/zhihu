# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class UserItem(scrapy.Item):
    #用户主页
    home_page = scrapy.Field()
    #用户类型
    user_page = scrapy.Field()
    #用户名
    name = scrapy.Field()
    #个性签名
    headline = scrapy.Field()
    #性别 0 代表女，1 代表男
    gender = scrapy.Field()
    #头像 url
    avatar_url = scrapy.Field()
    #回答数
    answer_count = scrapy.Field()
    #文章数
    articles_count = scrapy.Field()
    #问题数
    question_count = scrapy.Field()
    #获得赞同数
    voteup_count = scrapy.Field()
    #获得感谢数
    thanked_count = scrapy.Field()
    #参加 live 数
    participated_live_count = scrapy.Field()
    #参与公共编辑次数
    logs_count = scrapy.Field()
    #关注的话题数
    following_topic_count = scrapy.Field()
    #关注的问题数
    following_question_count = scrapy.Field()
    #关注的收藏夹
    following_favlists_count = scrapy.Field()
    #关注人数
    following_count = scrapy.Field()
    #粉丝人数
    follower_count = scrapy.Field()
    #被收藏次数
    favorited_count = scrapy.Field()
    #专栏数
    columns_count = scrapy.Field()
    #个人简介
    description = scrapy.Field()
    #收藏夹个数
    favorite_count = scrapy.Field()
    #关注的专栏个数
    following_columns_count = scrapy.Field()
    #想法条数
    pins_count = scrapy.Field()
    #举办live次数
    hosted_live_count = scrapy.Field()

    #url_token
    url_token = scrapy.Field()

    #教育经历
    educations = scrapy.Field()
    #职业经历
    employments = scrapy.Field()

    #居住地
    locations = scrapy.Field()
    #所处行业
    business = scrapy.Field()