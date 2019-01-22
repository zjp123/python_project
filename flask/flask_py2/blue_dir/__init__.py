#coding:utf-8

from flask import Blueprint

cart_app = Blueprint('cart_app', __name__, template_folder='templates')

from .views import getcart


# 在__init__.py 文件被执行的时候，把视图加载进来，让蓝图知道有视图的存在