import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Referer': 'https://hr.tencent.com/position.php?keywords=python&lid=2156&tid=0&start=0'
}

url = 'https://hr.tencent.com/position.php?keywords=python&lid=2156&tid=0&start=10#a'
host = 'https://hr.tencent.com/'
data = []

def splider():
    resp = requests.get(url, headers=headers)
    text = resp.content.decode('utf-8')
    html = etree.HTML(text)
    #infos = html.xpath("//table[@class='tablelist']//tr[contains(@class, 'odd')]//a/@href|//tr[contains(@class, 'even')]//a/@href")
    infos = html.xpath("//table[@class='tablelist']//td[contains(@class, 'square')]//a/@href")
    #print(infos)
    infos = map(lambda url:host + url, infos)
    #detail_url = list(infos)[0]
    for detail_url in infos:

        parse_url(detail_url)
    #print(html)

def parse_url(detail_url):
    print(detail_url)
    obj = {}

    resp = requests.get(detail_url, headers=headers)
    text = resp.content.decode('utf-8')
    html = etree.HTML(text)

    elements = html.xpath("//table[contains(@class, 'tablelist')]")[0]
    title = elements.xpath('.//tr[1]/td/text()')[0].strip()
    obj['title'] = title
    city = elements.xpath('.//tr[contains(@class, "bottomline")]/td[1]/text()')[0].strip()
    obj['city'] = city
    zhiwei = elements.xpath('.//tr[contains(@class, "bottomline")]/td[2]/text()')[0].strip()
    obj['zhiwei'] = zhiwei
    need_nums = elements.xpath('.//tr[contains(@class, "bottomline")]/td[3]/text()')[0].strip()
    obj['need_nums'] = need_nums

    zhize = elements.xpath('.//tr[3]/td/ul//text()')
    yaoqiu = elements.xpath('.//tr[4]/td/ul//text()')
    obj['zhize'] = ','.join(zhize)
    obj['yaoqiu'] = ','.join(yaoqiu)
    #print(zhize)
    print(obj)




if __name__ == "__main__":

    splider()