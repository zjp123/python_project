from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django_redis import get_redis_connection
from goods.models import GoodsSKU
from utils.minix import LoginCheck
# Create your views here.

# /cart/add
# 参数 sku_id count
class CartAdd(View):
    def post(self, req):

        # 用户是否登录
        if not req.user.is_authenticated():
            return  JsonResponse({'res':2, 'error': 'user not login'})

        # 获取参数
        sku_id = req.POST.get('sku_id')
        count = req.POST.get('count')
        # 校验数据
        if not all([sku_id, count]):
            return  JsonResponse({'res':0, 'error': 'data not all'})

        try:
            count = int(count)

        except Exception as e:

            return  JsonResponse({'res':1, 'error': 'data type error'})

        # 业务处理

        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist as e:
            return  JsonResponse({'res':3, 'error': 'the sale not in'})

        con = get_redis_connection('default')
        # 判断redis中是否已存在
        cart_key = 'cart_%d'%req.user.id
        cart_count = con.hget(cart_key, sku_id)
        if cart_count:
            count += cart_count

        # 校验商品库存
        if count > sku.stock:
            return  JsonResponse({'res':3, 'error': 'stock is not enough'})

        # 更新redis中的数据
        con.hset(cart_key, sku_id, count)
        total_count = con.hlen(cart_key)
        return JsonResponse({'res': 6, 'total_count':total_count, 'error': 'add success'})


# cart/info
class CartInfo(LoginCheck, View):
    def get(self, req):

        # 获取登录用户
        user = req.user
        cart_key = 'cart_%d'%user.id

        # 获取redis中存储的商品id
        con = get_redis_connection('default')

        skuids = con.hgetall(cart_key)
        skus = []
        total_jianshu = 0
        total_price = 0
        if skuids:
            for sku_id, count in skuids.items():

                sku = GoodsSKU.objects.get(id=sku_id)
                # 计算小计
                xiaoji = sku.price*int(count)
                sku.xiaoji = xiaoji
                sku.count = count
                skus.append(sku)
                total_jianshu += count
                total_price += xiaoji

        # 组织上下文
        context = {
            "skus":skus,
            'total_jianshu':total_jianshu,
            'total_price': total_price
        }

        return  render(req, 'cart.html', context)

# cart/update
class CartUpdate(View):
    def post(self, req):
        # 用户是否登录
        if not req.user.is_authenticated():
            return JsonResponse({'res': 0, 'error': 'user not login'})

        # 获取参数
        sku_id = req.POST.get('sku_id')
        count = req.POST.get('count')
        # 校验数据
        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'error': 'data not all'})

        try:
            count = int(count)

        except Exception as e:

            return JsonResponse({'res': 2, 'error': 'data type error'})

        # 业务处理

        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist as e:
            return JsonResponse({'res': 3, 'error': 'the sale not in'})

        # 校验商品库存
        if count > sku.stock:
            return JsonResponse({'res': 4, 'error': 'stock is not enough'})

        con = get_redis_connection('default')
        # 判断redis中是否已存在
        cart_key = 'cart_%d' % req.user.id

        con.hset(cart_key, sku_id, count)
        countVal = con.hvals(cart_key)
        total_count = 0
        for val in countVal:
            total_count += int(val)
        return JsonResponse({'res': 5, 'total_count':total_count, 'message': 'update sucess'})

# cart/delete
class CartDelete(View):
    def post(self, req):
        # 用户是否登录
        if not req.user.is_authenticated():
            return JsonResponse({'res': 0, 'error': 'user not login'})

        # 获取参数
        sku_id = req.POST.get('sku_id')

        # 校验数据
        if not all([sku_id]):
            return JsonResponse({'res': 1, 'error': 'data not all'})

        # 业务处理

        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist as e:
            return JsonResponse({'res': 5, 'error': 'the sale not in'})

        con = get_redis_connection('default')
        # 判断redis中是否已存在
        cart_key = 'cart_%d' % req.user.id
        con.hset(cart_key, sku_id, count)
        countVal = con.hvals(cart_key)
        total_count = 0
        for val in countVal:
            total_count += int(val)
        con.hdel(cart_key, sku_id)

        return JsonResponse({'res': 3, 'total_count':total_count, 'message': 'del success'})

