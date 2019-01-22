#encoding: utf-8

from urllib import parse

url = 'http://www.baidu.com?w=jsjjsjsj&name=jsjjs'
print(parse.urlsplit(url))