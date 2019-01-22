
from django.conf.urls import url
from goods import views

# 注意上下顺序是有影响的
urlpatterns = [
    url(r'^index$', views.index.as_view(), name='index'),
    url(r'^goods/(?P<goods_id>\d+)$', views.DetailView.as_view(), name='detail'),
    url(r'^list/(?P<type_id>\d+)/(?P<page>\d+)$', views.ListView.as_view(), name='detail'),
]
