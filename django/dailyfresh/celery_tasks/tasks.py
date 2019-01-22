from celery import Celery
from django.core.mail import send_mail
from django.conf import settings

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
django.setup()
# 这几个类要写在django导入后面，因为系统变量没生成之前，它是找不到的
from django.template import loader,RequestContext

from goods.models import GoodsType,IndexGoodsBanner,IndexPromotionBanner,IndexTypeGoodsBanner
# 第一个参数是任务代码的文件路径

app = Celery('celery_tasks.tasks', broker='redis://172.16.68.149:6379/8')

@app.task
def send_register_active_email(username, email, token):
    # 邮件主题
    subject = "天天生鲜激活"
    # 邮件正文
    message = ''
    html_message = '<h1>尊敬的用户%s, 欢迎你注册会员,请点击链接地址激活用户</h1><br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (username, token, token)
    # 发送人
    sender = settings.EMAIL_FROM
    # 接收列表
    recive = [email]
    send_mail(subject, message, sender, recive, html_message=html_message)


@app.task
def create_index_static_html():
    '''显示首页'''
    # 获取商品的种类信息
    types = GoodsType.objects.all()

    # 获取首页轮播商品信息
    goods_banners = IndexGoodsBanner.objects.all().order_by('index')

    # 获取首页促销活动信息
    promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

    # 获取首页分类商品展示信息
    for type in types:  # GoodsType
        # 获取type种类首页分类商品的图片展示信息
        image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
        # 获取type种类首页分类商品的文字展示信息
        title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')

        # 动态给type增加属性，分别保存首页分类商品的图片展示信息和文字展示信息
        type.image_banners = image_banners
        type.title_banners = title_banners

    # 组织模板上下文
    context = {'types': types,
               'goods_banners': goods_banners,
               'promotion_banners': promotion_banners
               }

    # 加载模板文件  返回模板文件对象
    tem = loader.get_template('static_index.html')
    # 定义模板上下文
    # con = RequestContext(req, tem)
    # 模板渲染
    static_html = tem.render(context)
    # 生成首页对应静态文件
    save_path = os.path.join(settings.BASE_DIR, 'static/index.html')
    with open(save_path, 'w') as f:
        f.write(static_html)
    # return render(request, 'index.html', context)