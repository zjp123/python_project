from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from user.models import User, Address
from goods.models import GoodsSKU
# from django.core.mail import send_mail
from order.models import OrderInfo,OrderGoods
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from celery_tasks.tasks import send_register_active_email
from django.http import HttpResponse
import re
from django.views.generic import View
from itsdangerous import  TimedJSONWebSignatureSerializer as Jiami, SignatureExpired
from utils.minix import LoginCheck
from django_redis import get_redis_connection
from django.conf import settings
# Create your views here.
# /user/register
def register(req):
    # 通过请求方式判断是注册处理还是请求页面
    if req.method == 'GET':

        return render(req, 'register.html')
    else:
        return register_handle(req)

def register_handle(req):

    username = req.POST.get('user_name')
    password = req.POST.get('pwd')
    email = req.POST.get('email')
    allow = req.POST.get('allow')
    if not all([username, password, email]):
        return render(req, 'register.html', {'erro': '数据不完整'})



    # 数据校验
    if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        return render(req, 'register.html', {'erro': '邮箱不正确'})

    if allow != 'on':
        return render(req, 'register.html', {'erro': '请选择用户协议'})

    try:
        user = User.objects.get(username=username)

    except User.DoesNotExist:
        user = None

    if not user:
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()
        #  发送激活链接 http://127.0.0.1:8000/user/active/3
        jiami = Jiami(settings.SECRET_KEY, 3600)
        info = {'zjp': user.id}
        token = jiami.dumps(info)
        token = token.decode()
        # 邮件主题
        # subject = "天天生鲜激活"
        # 邮件正文
        # message = ''
        # html_message = '<h1>尊敬的用户%s, 欢迎你注册会员,请点击链接地址激活用户</h1><br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>'%(username, token, token)
        # 发送人
        # sender = settings.EMAIL_FROM
        # 接收列表
        # recive = [email]
        # send_mail(subject, message, sender, recive, html_message=html_message)
        send_register_active_email.delay(username, email, token)
        # 返回应答  回到首页
        #return redirect(reverse('goods:index'))

    else:
        return render(req, 'register.html', {'erro': '用户名已存在'})

    '''
    user = User()
    user.username = username
    user.password = password
    user.email = email
    user.save()
    '''

    return redirect(reverse('goods:index'))

class Register(View):

    def get(self, req):
        return register(req)

    def post(self, req):
        return register_handle(req)



class ActiveUser(View):
    def get(self, req, token):
        try:
            jiemi = Jiami(settings.SECRET_KEY, 3600)
            info = jiemi.loads(token)
            id = info['zjp']
            id = int(id)
        except SignatureExpired as e:
            return HttpResponse('激活链接已过期')

        user = User.objects.get(id = id)
        user.is_active = 1
        user.save()

        return redirect(reverse('user:login'))


class Login(View):
    def get(self, req):

        username = req.COOKIES.get('username')
        if username:
            return render(req, 'login.html', {'username': username, 'checked': 'checked'})
        else:
            return render(req, 'login.html', {'username': '', 'checked': ''})


    def post(self, req):

        # 接收数据
        username = req.POST.get('username')
        password = req.POST.get('pwd')
        remerber = req.POST.get('remerber')
        # 校验数据
        if not all([username, password]):
            return render(req, 'login.html', {'error': '数据不完整'})

        # 处理业务
        user = authenticate(username=username, password=password)
        if user is not None:
            # 用户是否激活
            if user.is_active:
                login(req, user)

                # 获取登录后的url 就是之前没有登录时，让他登录，登录后要跳转的url，有些页面需要登录后才能访问
                # http://127.0.0.1:8000/user/login?next=/user/info
                # get函数若获取不到，会返回None，并且它还可以设置默认值，如果获取到默认值不生效
                next_url = req.GET.get('next', reverse('goods:index'))
                response = redirect(next_url)
                if remerber == 'on':
                    response.set_cookie('username', username, max_age=7*24*3600)
                else:
                    response.delete_cookie('username')

                return response
            else:
                return render(req, 'login.html', {'error': '账户未激活'})

        else:

            return render(req, 'login.html', {'error': '用户名或密码错误'})

# 用户信息 /user/info
class UserInfoView(LoginCheck, View):

    def get(self, req):
        user = req.user
        addr = Address.objects.get_default_addr(user)
        # 获取历史浏览记录
        #from redis import StrictRedis
        #red_cache = StrictRedis(host='172.16.68.145', port='6379', db=9)

        con = get_redis_connection('default')
        histroy_key = 'histroy_%d'%user.id
        skuids = con.lrange(histroy_key, 0 ,4)
        # 这样获取的查询集不是客户访问的先后顺序，还需要自己处理
        # goods = GoodsSKU.objects.filter(id__in = skuids)
        goods_list = []
        for id in skuids:
            goods = GoodsSKU.objects.get(id=id)
            goods_list.append(goods)

        return  render(req, 'user_center_info.html', {'page': 'info', 'addr': addr, 'goods': goods_list})


class LogoutView(View):
    def get(self, req):
        logout(req)

        return redirect(reverse('goods:index'))


# 用户订单 /user/order
class UserOrderView(LoginCheck, View):

    def get(self, req, page):
        # 来自django 的用户认证
        # req.user
        # 如果用户未登录req.user--->是AnonymousUser的一个实例
        # 如果用户登录是User的实例
        # req.user.is_authenticated() 返回true
        # 除了我们自己传给模板文件的变量外，django会把req的user属性也传给模板文件，可以在模板文件中直接使用
        user = req.user
        orders = OrderInfo.objects.filter(user=user).order_by('-create_time')

        # 遍历获取订单商品的信息
        for order in orders:
            # 根据order_id查询订单商品信息
            order_skus = OrderGoods.objects.filter(order_id=order.order_id)

            # 遍历order_skus计算商品的小计
            for order_sku in order_skus:
                # 计算小计
                amount = order_sku.count * order_sku.price
                # 动态给order_sku增加属性amount,保存订单商品的小计
                order_sku.amount = amount

            # 动态给order增加属性，保存订单状态标题
            order.status_name = OrderInfo.ORDER_STATUS[order.order_status]
            # 动态给order增加属性，保存订单商品的信息
            order.order_skus = order_skus

        # 分页
        paginator = Paginator(orders, 1)

        # 获取第page页的内容
        try:
            page = int(page)
        except Exception as e:
            page = 1

        if page > paginator.num_pages:
            page = 1

        # 获取第page页的Page实例对象
        order_page = paginator.page(page)

        # todo: 进行页码的控制，页面上最多显示5个页码
        # 1.总页数小于5页，页面上显示所有页码
        # 2.如果当前页是前3页，显示1-5页
        # 3.如果当前页是后3页，显示后5页
        # 4.其他情况，显示当前页的前2页，当前页，当前页的后2页
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)

        # 组织上下文
        context = {'order_page': order_page,
                   'pages': pages,
                   'page': 'order'}

        # 使用模板
        return render(req, 'user_center_order.html', context)


# 用户地址 /user/address
class UserAddressView(LoginCheck, View):

    def get(self, req):
        # 获取默认地址
        # req.user 是一个对象里面包含用户的信息
        user = req.user
        #print('***********************')
        #print(user.id)
        #print('***********************')

        addr = Address.objects.get_default_addr(user)

        return  render(req, 'user_center_site.html', {'page': 'address', 'addr': addr})

    def post(self, req):

        # 接收数据
        reciver = req.POST.get('reciver')
        addr = req.POST.get('addr')
        zip_code = req.POST.get('zip_code')
        phone = req.POST.get('phone')
        # 校验数据
        if not all([reciver, addr, phone]):
            return render(req, 'user_center_site.html', {'error': '数据不完整'})

        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
            return render(req, 'user_center_site.html', {'error': '手机格式不正确'})

        # 业务处理
        user = req.user
        try:
            is_default = Address.objects.get(user=user, is_default=True)
        except Address.DoesNotExist:
            is_default = False

        if not is_default:
            is_default = True
        else:
            is_default = False
        Address.objects.create(user=user, receiver=reciver, addr=addr,
                               zip_code=zip_code, phone=phone, is_default=is_default
                               )
        # 返回应答

        return redirect(reverse('user:address'))