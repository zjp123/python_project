# coding:utf-8

from flask import Flask, g, render_template
from flask_script import Manager


#g 全局存储空的容器
app = Flask(
        __name__,
        static_url_path = '/python', #默认是static
        static_folder = './static', # 静态文件目录
        template_folder = './templates'
)

@app.route('/index')
def index():

    return render_template('index.html', {"name": zjp, "age": 18})



# 自定义过滤器 第一种
def diy_list(li):

    return li[::2]
app.add_template_filter(diy_list, 'zjp')# 过滤器名称

# 第二种

@app.template_filter('ctt')
def diy_ctt(li):

    return li[::2]

if __name__ == "__main__":

    app.run(debug=True)