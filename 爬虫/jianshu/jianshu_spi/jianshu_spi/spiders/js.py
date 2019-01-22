# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu_spi.items import JianshuSpiItem


class JsSpider(CrawlSpider):
    name = 'js'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        title = response.xpath('//div[@class="article"]/h1[@class="title"]/text()').get()

        item = JianshuSpiItem(title=title)
        yield item
