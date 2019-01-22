# coding:utf-8

from flask import Flask, Blueprint

from blue_tu import app_stores
from blue_dir import cart_app



#g 全局存储空的容器
app = Flask(
        __name__,
        static_url_path = '/python', #默认是static
        static_folder = './static', # 静态文件目录
        template_folder = './templates'
)

# 它会把blue_tu里面的路由都会加上前缀/order
app.register_blueprint(app_stores, url_prefix='/order')
app.register_blueprint(cart_app, url_prefix='/cart')



if __name__ == "__main__":

    print(app.url_map)
    app.run()