# -*- coding: utf-8 -*-
import scrapy
from qsbk.items import QsbkItem

class QsbkSpiderSpider(scrapy.Spider):
    name = 'qsbk_spider'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1/']
    domain_url = 'https://www.qiushibaike.com'

    def parse(self, response):
        divs = response.xpath('//div[@id="content-left"]/div')
        for div in divs:
            author = div.xpath('.//h2/text()').get().strip()
            content = div.xpath('.//div[@class="content"]/span/text()').getall()
            content = "".join(content).strip()
            item = QsbkItem(author=author, content=content)
            yield item

        href = response.xpath('//ul[@class="pagination"]/li[last()]/a/@href').get()
        if not href:
            return
        else:
            nex_url = self.domain_url + href
            yield scrapy.Request(nex_url, callback=self.parse)