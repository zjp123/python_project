#encoding: utf-8

from urllib import request

resp = request.urlopen('http://www.baidu.com')

print(resp.read())
#resp.read(size) resp.readline() resp.readlines()  resp.getcode()