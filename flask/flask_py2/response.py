# coding:utf-8

from flask import Flask, make_response, jsonify
from werkzeug.routing import BaseConverter

import json


app = Flask(
        __name__,
        static_url_path = '/python', #默认是static
        static_folder = './static', # 静态文件目录
        template_folder = './templates'
)



@app.route('/index')
def index():

    # 使用元祖返回自定义信息

    #      响应体   状态码   响应头
    #  return  "999", "666 zjp", [("name", "tt"), ("age", 18)]

    # return 999, 500,  {"zjp":99, "age":20}
    # 使用 make_response 来构造响应信息
    resp = make_response("index page 2")
    resp.status = "999 diystatus" # 设置响应状态码
    resp.headers['kk'] = 'luanqibazao'
    return resp


def register():

    data = {
        "zjp": "zjp",
        "age": 20
    }

    # 转为json的简化操作
    return jsonify(data)