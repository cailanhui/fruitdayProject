import json

from django.core import serializers
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from .forms import *

def index_views(request):
    return render(request,'index.html')

# Create your views here.
def login_views(request):
    if request.method == 'GET':
        # 准备获取来访地址，如果没有则设置为'/'
        url = request.META.get('HTTP_REFERER','/')
        # 判断name和phone是否存进session
        if 'id' in request.session and 'phone' in request.session:
            # 从哪里来，回哪里去
            resp = HttpResponseRedirect(url)
            return resp
        else:
            # 否则，判断是否保存进cookies，若是则取出存进session，并返回首页
            if 'id' in request.COOKIES and 'phone' in request.COOKIES:
                id = request.COOKIES['id']
                phone = request.COOKIES['phone']
                request.session['id'] = id
                request.session['phone'] = phone
                # 从哪里来，回哪里去
                resp = redirect(url)
                return resp
            # 否则返回登录页面
            form = LoginForm()
            # 将来访地址保存进cookies中
            resp = render(request,'login.html',locals())
            resp.set_cookie('url',url)
            return resp
    else:
        # 取出登录页面请求
        form = LoginForm(request.POST)
        if form.is_valid():
            uphone = form.cleaned_data['uphone']
            upwd = form.cleaned_data['upwd']
            # 根据电话号码和密码判断用户是否存在
            users = User.objects.filter(uphone=uphone,upwd=upwd)
            if users:
                # 用户存在则将name和phone存进session
                request.session['id'] = users[0].id
                request.session['phone'] = users[0].uphone
                url = request.COOKIES.get('url','/')
                resp = redirect(url)
                # 将url从cookies中删除出去
                if 'url' in request.COOKIES:
                    resp.delete_cookie('url')
                # 判断是否保勾选保存，若是，则将用户id和phone保存进cookies
                if 'isSaved' in request.POST:
                    resp.set_cookie('id',users[0].id,60*60*24)
                    resp.set_cookie('phone', uphone, 60 * 60 * 24)
                return resp
            return HttpResponse('密码错误')

def register_views(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        # uphone = request.POST['uphone']
        # users = User.objects.filter(uphone=uphone)
        # if not users:
        #     upwd = request.POST['pwd']
        #     uname = request.POST['uname']
        #     uemail = request.POST['uemail']
        #     user = User()
        #     user.uphone = uphone
        #     user.upwd = upwd
        #     user.uname = uname
        #     user.uemail = uemail
        #     user.save()
        #     request.session['id'] = user.id
        #     request.session['phone'] = user.uphone
        #     return HttpResponse('注册成功')
        # else:
        #     errMsg = '手机号码已被注册'
        #     return HttpResponse(errMsg)
        data = request.POST
        user = User()
        user.uname = request.POST['uname']
        user.upwd = request.POST['upwd']
        user.uphone = request.POST['uphone']
        user.uemail = request.POST['uemail']
        user.save()
        # 取出user中id和uphone的值保存进session
        request.session['id'] = user.id
        request.session['phone'] = user.uphone
        return HttpResponse('OK')

# 检查手机号师傅已经被注册
def check_uphone_views(request):
    # 接收前端传递过来的数据
    uphone = request.GET['uphone']
    user = User.objects.filter(uphone=uphone)
    if user:
        status = 1
        msg = '手机号码已被注册'
    else:
        status = 0
        msg = '通过'
    dic = {
        'status':status,
        'msg':msg,
    }
    return HttpResponse(json.dumps(dic))

# 检查session中是否有登录信息，如果有则获取对应数据的uname的值
def check_login_views(request):
    if 'id' in request.session and 'phone' in request.session:
        loginStatus = 1
        # 通过id的值获取对应的uname
        id = request.session['id']
        uname = User.objects.get(id=id).uname
        dic = {
            'loginStatus':loginStatus,
            'uname':uname,
        }
        return  HttpResponse(json.dumps(dic))
    else:
        dic = {
            'loginStatus':0,
        }
        return HttpResponse(json.dumps(dic))


def logout_views(request):
    if 'id' in request.session and 'phone' in request.session:
        del request.session['id']
        del request.session['phone']
        # 构建响应对应，哪里发出请求则返回哪里
        url = request.META.get('HTTP_REFERER','/')
        resp = HttpResponseRedirect(url)
        # 判断cookies中是否有登录信息，有的话，则删除
        if 'id' in request.COOKIES and 'phone' in request.COOKIES:
            resp.delete_cookie('id')
            resp.delete_cookie('phone')
            return resp
    return redirect('/')

# 加载所以得商品类型以及对于的每个类型下的前10条数据
def goods_type_views(request):
    all_list = []
    # 加载所有的商品类型
    types = GoodsType.objects.all()
    for type in types:
        type_json = json.dumps(type.to_dict())
        #获取type类型下的最新的10条数据
        goods_list = type.goods_set.order_by('-id')[0:10]
        #将goods_list转换为json
        goods_list_json = serializers.serialize('json',goods_list)
        #将type_json和goods_list.json封装到一个字典中
        dic = {
            'type':type_json,
            'goods':goods_list_json,
        }
        all_list.append(dic)
    return HttpResponse(json.dumps(all_list))

# 将商品加入购物车或更新商品数量
def add_cart_views(request):
    good_id = request.GET['id']
    user = request.session['id']
    carts = CartInfo.objects.filter(user_id=user,goods_id=good_id)
    if carts:
        # CartInfo.objects.filter(goods=good_id,user=user).update(count=F('count')+1)
        cart = carts[0]
        cart.count = cart.count + 1
        cart.save()
        dic = {
            'status':1,
            'statusText':'更新数量成功',
        }
    else:
        cart = CartInfo()
        cart.user_id = user
        cart.goods_id = good_id
        cart.count = 1
        cart.save()
        dic = {
            'status':1,
            'statusText':'添加购物车成功'
        }
    return HttpResponse(json.dumps(dic))










