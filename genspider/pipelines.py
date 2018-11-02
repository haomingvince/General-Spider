# -*- coding: utf-8 -*-
'''
制作人: 张浩铭
参与者: 张浩铭
时间: 2018.07
版本号: v1.0
内容描述: 爬虫运行中间件，负责控制输出形式，此文件暂定输出为json
'''
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class GenspiderPipeline(object):
    def process_item(self, item, spider):
        file = open('out.json', 'a', encoding='utf-8')
        line = json.dumps(dict(item), ensure_ascii=False)+"\n"
        file.write(line)  # 以 json 的格式写入
        return item