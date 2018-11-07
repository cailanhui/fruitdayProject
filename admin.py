from django.contrib import admin
from .models import *


class GoodsAdmin(admin.ModelAdmin):
    #指定在列表页中所显示的字段闷
    list_display = ('title','goodstype','price','spec')
    #指定右侧显示的过滤器
    list_filter = ('goodstype',)
    #指定在上方显示的字段
    search_fields = ('title',)

# Register your models here.
admin.site.register(User)
admin.site.register(GoodsType)
admin.site.register(Goods,GoodsAdmin)
admin.site.register(CartInfo)
