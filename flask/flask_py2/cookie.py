# coding:utf-8

from flask import Flask, make_response, request



app = Flask(
        __name__,
        static_url_path = '/python', #默认是static
        static_folder = './static', # 静态文件目录
        template_folder = './templates'
)


@app.route('/set_cookie')
def set_cookie():

    resp = make_response("set cookie")
    resp.set_cookie('zjp', 'ok')
    resp.set_cookie('xiongdi', 'okokok', max_age=3600)

    return resp



@app.route('/get_cookie')
def get_cookie():

    coo = request.cookies.get('zjp')

    return coo



@app.route('/delete_cookie')
def delete():

    resp = make_response('delete cookie')

    resp.delete_cookie('zjp')

    return resp







if __name__ == "__main__":

    app.run(debug=True)