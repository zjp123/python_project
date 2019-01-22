# coding:utf-8

from flask import Flask, current_app, redirect, url_for, request
from werkzeug.routing import BaseConverter

#current_app 相当于app的全局变量
# redirect 跟django里面的一个意思
# url_for 跟django里面的reverse一个意思,所需要的name就是定义的处理函数的名字
# request 处理请求的 request.data request.form request.args
# request.form.getlist('key') 可以获取多个同键名的请求字段
# request.files.get(key) 获取上传的文件对象
app = Flask(
        __name__,
        static_url_path = '/python', #默认是static
        static_folder = './static', # 静态文件目录
        template_folder = './templates'
)

# 使用配置文件 设置配置参数

# app.config.from_pyfile('./config.cfg')

# 使用对象进行配置

'''

class CONFIG(object):
    DEBUG = True
    zjp = 666
    
app.config.from_object(CONFIG)
'''

app.config['DEBUG'] = True

@app.route('/', methods=["POST", "GET"])
def index():

   # a = 1 / 0
    # print(app.config.get('zjp')) 可以拿到值
    return "nihao "

# 这两个路径都可以返回666
@app.route('/zjp')
@app.route('/zjp2')
def zjp():
    return 666;


# 路由转换器
# 127.0.0.1/goods/123
@app.route('/goods/<int:goods_id>')
def goods(goods_id):

    pass

# 自定义路由转换器

class Mobile(BaseConverter):

    def __init__(self, url_map, regex):

        super(Mobile, self).__init__(url_map)
        # 把正则表达式参数保存在对象属性中， flask会使用这个属性进行验证
        self.regex = regex

    def to_python(self, value):
        ''' 在转换器解析之前被调用'''
        return value

    def to_url(self, value):
        ''' 在使用url_for 的时候被调用'''
        return value


app.url_map.converters['re'] = Mobile

@app.route('/mobile/<re(r"1[3|5]\d{9}"):mobilenum>')
def ordernum(moblienum):
    pass


def tiaozhuan():

    url = url_for('ordernum', mobilenum='12345678')

    return redirect(url)



#width 上下文管理器

class Foo(object):

    def __enter__(self):
        '''进入width语句被调用'''

        print('jinru')

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''width语句结束时候被调用'''
        print('likai')





if __name__ == "__main__":

    app.run()
    # app.run(host='0.0.0.0', port='5000')