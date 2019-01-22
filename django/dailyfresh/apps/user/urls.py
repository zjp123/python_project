
from django.conf.urls import url
from user import views
# 借用django里面的函数 来判断用户是否登录过，因为有的页面没有登录是不可以访问的
from django.contrib.auth.decorators import login_required
# from user.views import Register, ActiveUser
# 注意上下顺序是有影响的
urlpatterns = [
    # url(r'^register$', Register.as_view(), name='register'),
    url(r'^register$',  views.register, name='register'),
    url(r'^register_handle$', views.register_handle),
    url(r'^active/(?P<token>.*)$', views.ActiveUser.as_view(), name='active'), # 激活用户
    url(r'^login$', views.Login.as_view(), name='login'),  # 激活用户
    url(r'^logout', views.LogoutView.as_view(), name='logout'),  # 用户退出
    #url(r'^info$', login_required(views.UserInfoView.as_view()), name='info'),  # 激活用户
    #url(r'^order$', login_required(views.UserOrderView.as_view()), name='order'),  # 激活用户
    #url(r'^address$', login_required(views.UserAddressView.as_view()), name='address'),  # 激活用户
    url(r'^info$', views.UserInfoView.as_view(), name='info'),  # 激活用户
    url(r'^order/(?P<page>\d+)$', views.UserOrderView.as_view(), name='order'),  # 用户中心-订单页
    url(r'^address$', views.UserAddressView.as_view(), name='address'),  # 激活用户

]
