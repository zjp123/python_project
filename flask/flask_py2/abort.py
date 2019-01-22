# 自定义错误处理信息

# coding:utf-8

from flask import Flask, current_app, redirect, url_for, request
from werkzeug.routing import BaseConverter


app = Flask(
        __name__,
        static_url_path = '/python', #默认是static
        static_folder = './static', # 静态文件目录
        template_folder = './templates'
)


#它会捕捉系统或者abort抛出的404的错误，然后把返回值交给系统，可以修改对应的状态码
@app.errorhandler(404)
def login():

    return "kskkkkskk"


if __name__ == "__main__":

    app.run(debug=True)