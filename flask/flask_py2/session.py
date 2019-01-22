# coding:utf-8

from flask import Flask, session



app = Flask(
        __name__,
        static_url_path = '/python', #默认是static
        static_folder = './static', # 静态文件目录
        template_folder = './templates'
)
# 使用session时，需要设置秘钥

app.config['SECRET_KEY'] = 'sojsderuennbnkebni,,##*0o3'

#flask默认把session存储cookie中，可以通过配置使其存储在后端数据库中

@app.route('/login')
def login():
    # 设置session
    session['name'] = 'zjp'

    return "login sucess"



@app.route('/index')
def index():
    # 获取session
    name = session.get('name')

    return 'get name'



if __name__ == "__main__":

    app.run(debug=True)