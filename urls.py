from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^login/$',login_views,name='login'),
    url(r'^register/$',register_views,name='register'),
    url(r'^$',index_views),
    url(r'^check_uphone/$',check_uphone_views),
    url(r'^check_login/$',check_login_views),
    url(r'^logout/$',logout_views),
    url(r'^load_goods_type/$',goods_type_views),
    url(r'^add_cart/$',add_cart_views),

]
