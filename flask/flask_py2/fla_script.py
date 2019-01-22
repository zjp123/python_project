# coding:utf-8

from flask import Flask, g
from flask_script import Manager


#g 全局存储空的容器
app = Flask(
        __name__,
        static_url_path = '/python', #默认是static
        static_folder = './static', # 静态文件目录
        template_folder = './templates'
)


manage = Manager(app)




if __name__ == "__main__":


    manage.run()