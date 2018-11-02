# -*- coding: utf-8 -*-
'''
制作人: 张浩铭
参与者: 张浩铭
时间: 2018.07
版本号: v1.0
内容描述: 爬虫field，简而言之为爬虫爬取的内容暂时储存地
'''
# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GenspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()  # 新闻链接
    title = scrapy.Field() # 新闻标题
    source = scrapy.Field() # 新闻来源/作者
    time = scrapy.Field() # 发布时间
    content = scrapy.Field() # 新闻内容
    pass
