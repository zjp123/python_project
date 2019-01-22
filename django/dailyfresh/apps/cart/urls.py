
from django.conf.urls import url
from cart.views import CartAdd, CartInfo, CartUpdate, CartDelete
# 注意上下顺序是有影响的
urlpatterns = [
    url(r'^add$', CartAdd.as_view(), name='add'),
    url(r'^info$', CartInfo.as_view(), name='info'),
    url(r'^update', CartUpdate.as_view(), name='update'),
    url(r'^delete', CartDelete.as_view(), name='delete'),

]
