# -*- coding: utf-8 -*-
import scrapy
import re
from fangtianxia.items import FangtianxiaItem, ESFitem

class FangSpider(scrapy.Spider):
    name = 'fang'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def parse(self, response):

        trs = response.xpath('.//div[@class="outCont"]//tr')
        privince = None

        for tr in trs:
            tds = tr.xpath('.//td[not(@class)]')
            privince_text  = tds[0].xpath('.//text()').get().strip()

            if privince_text:
                privince = privince_text

            if privince == "其它":
                continue

            city_tds = tds[1].xpath('.//a')

            for city in city_tds:
                cityname = city.xpath('./text()').get()
                cityurl = city.xpath('./@href').get()
                #http://wuhu.fang.com/
                htp = cityurl.split(':')[0]
                host = cityurl.split(':')[1]
                #print("省份：%s" % privince)
                #print("城市：%s, 链接： %s" % (cityname, cityurl))
                newhouse_url = None
                eshouse_url = None



                if cityname == "昌吉":
                    newhouse_url = 'https://changji.newhouse.fang.com/house/s/'
                    eshouse_url = cityurl

                else:
                    city_pinyin = re.findall(r'(http|https)://(\w+)(.fang.com|.esf.fang.com)/?', cityurl)
                    city_pinyin = city_pinyin[0][1]
                    # https://sh.esf.fang.com/
                    # https://sh.newhouse.fang.com/house/s/

                    newhouse_url = 'https://' + city_pinyin + '.newhouse.fang.com/house/s/'
                    eshouse_url = 'https://' + city_pinyin + '.esf.fang.com/'

                if cityname == "北京":
                    #https: // newhouse.fang.com / house / s /
                    newhouse_url = 'https://newhouse.fang.com/house/s/'
                    eshouse_url = 'https://esf.fang.com'


                #print('城市：新房url:%s,旧房url:%s' %(newhouse_url, eshouse_url))
                yield scrapy.Request(url = newhouse_url, callback=self.parse_newhouse, meta={"info": (privince, cityname)})
                yield scrapy.Request(url = eshouse_url, callback=self.parse_esf, meta={"info": (privince, cityname)})
                break
            break

    def parse_newhouse(self, response):
        prinvice, cityname = response.meta.get('info')

        # print(666)
        lis = response.xpath('.//div[@id="newhouse_loupai_list"]/ul/li')
        for li in lis:

            name = li.xpath('.//div[@class="nlcd_name"]/a/text()').get()
            if name:
                name = name.strip()

            address = li.xpath('.//div[@class="address"]/a/@title').get()
            price = li.xpath('.//div[@class="nhouse_price"]/span/text()').get()
            if price:

                price = price + '元/㎡'
            rooms = li.xpath('.//div[@class="house_type clearfix"]//text()').getall()
            rooms = list(filter(lambda x:x.endswith("居"), rooms))
            rooms = "".join(rooms)
            area = list(li.xpath('.//div[@class="house_type clearfix"]//text()').getall())
            if area:
                area = area[-1]
                area = re.sub(r"\s|－", "", area)
            # if type(area) == 'str':
            #
            #     area = area.strip().replace(r'－|\s|－', '').strip()
            #area = list(filter(lambda x:re.sub(r'\s|-', "",x), rooms))

            item = FangtianxiaItem(prinvice=prinvice,city=cityname,name=name,rooms=rooms,address=address,area=area)
            print(name)
            print(area)
            print('*'*20)
            yield item

        nex_url = response.xpath('.//div[@class="page"]/a[@class="next"]/@href')
        if nex_url:
            yield scrapy.Request(url=response.urljoin(nex_url), callback=self.parse_newhouse, meta={"info": (prinvice, cityname)})


    def parse_esf(self, response):

        prinvice, city = response.meta.get('info')
        item = ESFitem(province=prinvice, city=city)
        dls = response.xpath('.//div[@class="shop_list shop_list_4"]/dl')

        for dl in dls:
            name = dl.xpath('.//p[@class="add_shop"]/a/@title').get()
            item['name'] = name
            item['address'] = dl.xpath('.//p[@class="add_shop"]/span/text()').get()
            item['price'] = dl.xpath('./dd[@class="price_right"]/span[2]/text()').get()
            infos = dl.xpath('.//p[@class="tel_shop"]//text()').getall()
            infos = list(map(lambda x:re.sub(r"\s|\|", "", x), infos))
            for info in infos:
                if "厅" in info:
                    item['rooms'] = info

                elif '㎡' in info:
                    item['area'] = info

                yield item


        next_url = response.xpath('.//div[@class="page_al"]//p')[-3]
        next_url = next_url.xpath('./a/@href').get()

        yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse_esf, meta={"info": (prinvice, city)})
        # print(next_url)
