# -*- coding: utf-8 -*-
'''
制作人: 张浩铭
参与者: 张浩铭
时间: 2018.07
版本号: v1.0
内容描述: 爬虫主体。所有爬虫相关的函数都在此文件中。
'''
import scrapy
import re
import ast # reference to: https://stackoverflow.com/questions/1894269/convert-string-representation-of-list-to-list
from scrapy.linkextractor import LinkExtractor
from genspider.items import GenspiderItem
from scrapy.spiders import Rule
from pprint import pprint as pp


class genSpider(scrapy.Spider):
    name = 'genspider'
    news_list_names = ["信息中心", "新闻中心", "新闻动态", "资讯聚焦"]
    news_content_list_names = ["重要通知", "停气信息", "新闻动态", "招标公告", "招聘信息", "要闻在线", "工作动态", "区县风采", "新女性", "热点专题", 
    "集团新闻", "通知公告", "企业动态", "领导视察", "媒体报道", "国企改革"] # 亟待更新，仅限测试使用
    exist_list = set()  # 链接去重
    
    def __init__(self, augment=None, *args, **kwargs):  # 实现传参 refrence to: https://blog.csdn.net/q_an1314/article/details/50748700
        super(eval(self.__class__.__name__), self).__init__(*args, **kwargs)
        self.start_urls = ast.literal_eval(augment) # 转换传入参数

    def start_requests(self):
        for url in self.start_urls:   # 异步进入各个根网页
            print("#################### root url: ", url)
            yield scrapy.Request(url, self.parse)

    def parse(self, response): # 进入官网，再进入各个新闻列表主页
        for news_list_name in self.news_list_names:
            try:
                pat = r"<a.*?href=\"(.*?)\".*?>\s*\n?" + news_list_name + r"\s*</a>"  # 根据给定关键词查找对应新闻页面的 href
                ma = re.findall(pat, response.text)[0]
                # TODO: 无法爬取a标签中带换行的页面
                if "http" in ma:
                    url = ma
                else:
                    url = response.url[:-1] + ma     # 重要！！！response.url 返回的最后一个 '/' 与 regex找的href 第一个 '/'重复，必须去掉一个'/'
                if url not in self.exist_list:
                    self.exist_list.add(url)
                    print("################### news list: ", url)
                    yield scrapy.Request(url, callback=self.parse_content_list)
            except:
                pass
    
    def parse_content_list(self, response): # 进入新闻列表之后 找到各个新闻分列表
        for news_content_list_name in self.news_content_list_names:
            try:
                pat1 = r"<a[^>]*?>" + news_content_list_name + r"</a>" # 根据给定关键词查找对应新闻页面的标签信息 Ref: https://stackoverflow.com/questions/44122153/python-non-greedy-regular-expression-searching-too-many-data
                ma1 = re.findall(pat1, response.text)[0]
                sub_name = re.findall(r"href=\"(.*?)\"", ma1)[0] # 获得 href
                pat2 = r"(http://.*?/)"
                ma2 = re.findall(pat2, response.url)[0]
                if "http" in sub_name:
                    url = sub_name
                else:
                    url = ma2 + sub_name
                if url not in self.exist_list:
                    self.exist_list.add(url)
                    print("#################### content list: ", url)
                    # yield scrapy.Request(url, callback=self.parse_pages)   # 如果要加入翻页 请删除下一行并接触本行注释
                    yield scrapy.Request(url, callback=self.parse_list)   # 暂时跳过翻页操作
            except:
                pass

    # TODO: 找到翻页的规律
    # def parse_pages(self, response): # 进入新闻分列表后 执行翻页操作
    #     maxPage = 0
    #     content = response.css(".pager")
    #     for href in content.css("a::attr(href)").extract():   # 找到当前分页的最大页码
    #         temp = int(re.findall(r"\d+", href)[0])
    #         if temp >= maxPage:
    #             maxPage = temp
    #     for i in range(1, maxPage+1):   # 进入每一个页码页面
    #         url = response.url + "?currentPage=" + str(i)
    #         print(url)
            # yield scrapy.Request(url, callback=self.parse_list): # 进入分类

    def parse_list(self, response):   # 爬取新闻链接 TODO: 有些网址的导航栏的结构也是 ul li 无法过滤
        content = response.css("ul li").extract()
        for everything in content:
            try:
                ma = re.findall(r"href=\"(.*?)\"", everything)[0].replace("&amp;", "&")  # 替换 &amp; 为 &
                pat2 = r"(http://.*?/)"
                ma2 = re.findall(pat2, response.url)[0]
                if "http" in ma:
                    url = ma
                else:
                    url = ma2 + ma
                if url not in self.exist_list:
                    self.exist_list.add(url)
                    # print(url)
                    yield scrapy.Request(url, callback=self.parse_news)
            except:
                continue

    def parse_news(self, response):   # 获得新闻正文以及相关数据
        item = GenspiderItem()
        print("\nNow parsing: {}\n".format(response.url))
        item["url"] = response.url
        try:
            item["title"] = response.xpath("//h1/text()").extract()[0]
        except:
            item["title"] = "------"
        try:    
            # content_temp = response.xpath('//*[@id="news-content"]/p/text() | //*[@id="news-content"]/p/strong/text() | //*[@id="news-content"]/p/span/text() | //*[@id="news-content"]/text()').extract()
            content_temp = response.xpath('//p/text() | //p/strong/text() | //p/span/text()').extract()
            for i in range(len(content_temp)):
                content_temp[i] = content_temp[i].replace(u'\xa0', u' ').strip()
            item["content"] = "".join(content_temp)
        except:
            item["content"] = "------"
        try:
            item["time"] = re.findall(r"\d{4}-\d{2}-\d{2}", response.text)[0]
        except:
            item["time"] = "------"
        try:
            item["source"] = re.findall(r"来源：(.*?)<", response.text)[0]
        except:
            item["source"] = "---"
        print("title: {} \ntime: {} \ncontent: {} \nurl: {}\n".format(item["title"], item["time"], item["content"], item["url"]))
        if item["content"] == "------" or item["content"] == "":
            pass
        else:
            return item