import requests
from lxml import etree
import re
import os
from urllib import request

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}




def main():

    res = requests.get('http://www.doutula.com/photo/list/?page=1')
    text = res.text

    html = etree.HTML(text)
    #print(etree.tostring(html).decode('utf-8'))

    imgs = html.xpath('//div[@class="page-content text-center"]//img[@class!="gif"]')
    for img in imgs:
       # print(etree.tostring(img))
       imgurl = img.get('data-original')
       imgurl = imgurl[:-4]
       alt = img.get('alt')
       alt = re.sub(r'[\.\?？,.。!！\*]', '', alt)
       suffix = os.path.splitext(imgurl)[1]
       request.urlretrieve(imgurl, 'images/%s'%(alt + suffix))
       print(imgurl)
       print(alt)
       print(suffix)


if __name__ == '__main__':
    main()