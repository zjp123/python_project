from django.contrib import admin
from goods.models import GoodsType, IndexGoodsBanner, IndexTypeGoodsBanner, IndexPromotionBanner
from django.core import cache
# Register your models here.


class BaseModelManage(admin.ModelAdmin):
    '''当用户新增一条数据点击保存时自动触发'''
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # 发出任务 让celery发出任务 重新生成首页静态文件
        from celery_tasks.tasks import create_index_static_html
        create_index_static_html.delay()

        # 删除缓存
        cache.delete('goods_index_data')

    '''当用户删除一条数据点击保存时自动触发'''
    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        # 发出任务 让celery发出任务 重新生成首页静态文件
        from celery_tasks.tasks import create_index_static_html
        create_index_static_html.delay()
        # 删除缓存
        cache.delete('goods_index_data')


class GoodsTypeManage(BaseModelManage):
    pass


class IndexGoodsBannerManage(BaseModelManage):
    pass



class IndexTypeGoodsBannerManage(BaseModelManage):
    pass


class IndexPromotionBannerManage(BaseModelManage):
    pass

admin.site.register(GoodsType, GoodsTypeManage)
admin.site.register(IndexGoodsBanner, IndexGoodsBannerManage)
admin.site.register(IndexTypeGoodsBanner, IndexTypeGoodsBannerManage)
admin.site.register(IndexPromotionBanner, IndexPromotionBannerManage)