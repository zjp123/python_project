# coding:utf-8

from flask import Flask, session, url_for, g


#g 全局存储空的容器
app = Flask(
        __name__,
        static_url_path = '/python', #默认是static
        static_folder = './static', # 静态文件目录
        template_folder = './templates'
)



@app.route('/index')
def index():

    return 'index 1'



# 这些钩子是不区分什么请求路径的，只要有请求过来就会被执行
# 在第一次请求处理之前执行
@app.before_first_request
def handle_first_before():

    print('第一次之前被执行')


# 在请求(视图处理函数)处理之前执行
@app.before_request
def handle_request_before():
    print('请求之前被执行')




# 在请求(视图处理函数)处理后
@app.after_request
def handle_request_after(res):
    print('请求之后调用')

    return res




# z最后执行
@app.teardown_request
def handle_request_zuihou(res):
    # 这个函数要在debug为false的时候
    print('请求最后调用')
    if path == url_for('/index'):
        print(99)
    return res





if __name__ == "__main__":

    app.run(debug=True)