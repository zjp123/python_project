# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exporters import JsonItemExporter #这种是返回的数组，把返回的数据一次性返回，适用于数据量比较小的
from scrapy.exporters import JsonLinesItemExporter #一行一行的返回适用于数据量比较大的


# class QsbkPipeline(object):
#
#     def __init__(self):
#         self.fp = open("duanzi.json", 'w',encoding='utf-8')
#
#     def open_spider(self,spider):
#         print('爬虫开始了...')
#
#     def process_item(self, item, spider):
#         item_json = json.dumps(dict(item),ensure_ascii=False)
#         self.fp.write(item_json+'\n')
#         return item
#
#     def close_spider(self,spider):
#         self.fp.close()
#         print('爬虫结束了...')

class QsbkPipeline(object):

    def __init__(self):
        self.fp = open("duanzi.json", 'wb')
        self.exporter = JsonLinesItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')

    def open_spider(self,spider):
        print('爬虫开始了...')

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self,spider):
        self.fp.close()
        print('爬虫结束了...')