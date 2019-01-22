#encoding: utf-8

from urllib import request

#url = 'https://weibo.com/aj/v6/user/uid?is_sync=1'
url = 'http://wimg.spriteapp.cn/pc/jwplayer/skin/five-audio.xml'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',


}

req = request.Request(url, headers=headers)

resp = request.urlopen(req)

with open('test.html', 'w', encoding='utf-8') as fp:
    fp.write(resp.read().decode('utf-8'))