
from django.conf.urls import url
from order.views import OrderPlace, OrderCommit, OrderPayView, CheckPayView, CommentView
# 注意上下顺序是有影响的
urlpatterns = [
    url(r'^place$', OrderPlace.as_view(), name='place'),
    url(r'^commit$', OrderCommit.as_view(), name='commit'),
    url(r'^pay$', OrderPayView.as_view(), name='pay'),
    url(r'^check$', CheckPayView.as_view(), name='check'),
    url(r'^commit/(?P<order_id>.+)$', CommentView.as_view(), name='commit'),

]
