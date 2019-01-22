from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.core.cache import cache
from django.core.paginator import Paginator
from goods.models import GoodsType,IndexGoodsBanner,IndexPromotionBanner,IndexTypeGoodsBanner, GoodsSKU
from order.models import OrderGoods, OrderInfo
from django_redis import get_redis_connection
from utils.minix import LoginCheck
# Create your views here.

# class Test(object):
#     def __init__(self):
#         self.name = 'abc'
#
# t = Test()
# t.age = 10
# print(t.age)


# http://127.0.0.1:8000
class index(View):
    '''首页'''
    def get(self, request):
        # 获取缓存
        user = request.user
        context = cache.get('goods_index_data')
        if context is None:

            '''显示首页'''
            # 获取商品的种类信息
            types = GoodsType.objects.all()

            # 获取首页轮播商品信息
            goods_banners = IndexGoodsBanner.objects.all().order_by('index')

            # 获取首页促销活动信息
            promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

            # 获取首页分类商品展示信息
            for type in types: # GoodsType
                # 获取type种类首页分类商品的图片展示信息
                image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
                # 获取type种类首页分类商品的文字展示信息
                title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')

                # 动态给type增加属性，分别保存首页分类商品的图片展示信息和文字展示信息
                type.image_banners = image_banners
                type.title_banners = title_banners

            # 设置缓存
            print('设置缓存')
            # 组织模板上下文
            context = {'types': types,
                       'goods_banners': goods_banners,
                       'promotion_banners': promotion_banners,
                       'user':user
                       }
            cache.set('goods_index_data', context, 3600)
        # 获取用户购物车中商品的数目
        user = request.user
        cart_count = 0
        if user.is_authenticated():
            # 用户已登录
            conn = get_redis_connection('default')
            cart_key = 'cart_%d'%user.id
            cart_count = conn.hlen(cart_key)

        # 组织模板上下文
        context.update(cart_count=cart_count)

        # 使用模板
        return render(request, 'index.html', context)

# goods/商品id
class DetailView(View):
    '''详情页'''
    def get(self, req, goods_id):
        '''显示详情页'''

        # 获取商品具体详情信息
        try:
            sku = GoodsSKU.objects.get(id=goods_id)
        except GoodsSKU.DoesNotExist:
            return redirect(reverse('goods:index'))

        # 获取商品种类信息
        types = GoodsType.objects.all()

        # 获取商品评论  过滤评论为空的
        commnt = OrderGoods.objects.filter(sku=sku).exclude(comment='')

        #获取新品信息

        newsp = GoodsSKU.objects.filter(type=sku.type).order_by('-create_time')[:2]

        # 获取同一个spu的其他规格产品信息

        otherspu = GoodsSKU.objects.filter(goods=sku.goods).exclude(id=goods_id)

        # 获取用户购物车中商品的数目
        user = request.user
        cart_count = 0
        if user.is_authenticated():
            # 用户已登录
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id
            cart_count = conn.hlen(cart_key)

        context = {'types': types,
                   'commnt': commnt,
                   'newsp': newsp,
                   'cart_count': cart_count,
                   'otherspu': otherspu
                   }
        return render(req, 'detail.html', context)


# 种类id 页码 排序方式

# list/type_id/page?sort=xx 问号后面不参与url的配置，可以通过req.get('sort')方式捕获
class ListView(View):

    def get(self, req, type_id, page):


        # 获取当前type
        try:
            type = GoodsType.objects.get(id=type_id)
        except Exception as e:
            return redirect(reverse('goods:index'))

        # 获取全部种类
        alltypes = GoodsType.objects.all()

        # 获取新品：
        newstype = GoodsSKU.objects.filter(type=type).order_by('-create_time')[:2]

        # 获取排序方式
        sort = req.GET.get('sort')
        if sort not in ['id', 'sales', 'price']:
            sort = 'id'

        # 获取当前种类下的全部商品

        allsku = GoodsSKU.objects.filter(type=type).order_by(sort)

        # 分页
        pageobj = Paginator(allsku, 1)

        # 获取page的内容
        try:
            page = int(page)
        except Exception as e:
            page = 1

        if page > pageobj.num_pages:
            page = 1
        # 获取第page的实例对象
        the_page = pageobj.page(page)
        user = request.user
        cart_count = 0
        if user.is_authenticated():
            # 用户已登录
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id
            cart_count = conn.hlen(cart_key)

        context = {'type': type,
                   'alltypes': alltypes,
                   'newstype': newstype,
                   'cart_count': cart_count,
                   'page': the_page,
                   'sort': sort
                   }

        render(req, 'list.html')

# /user/order
class UserOrderView(LoginCheck, View):
    '''用户中心-订单页'''
    def get(self, request, page):
        '''显示'''
        # 获取用户的订单信息
        user = request.user
        orders = OrderInfo.objects.filter(user=user).order_by('-create_time')

        # 遍历获取订单商品的信息
        for order in orders:
            # 根据order_id查询订单商品信息
            order_skus = OrderGoods.objects.filter(order_id=order.order_id)

            # 遍历order_skus计算商品的小计
            for order_sku in order_skus:
                # 计算小计
                amount = order_sku.count*order_sku.price
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
        context = {'order_page':order_page,
                   'pages':pages,
                   'page': 'order'}

        # 使用模板
        return render(request, 'user_center_order.html', context)

