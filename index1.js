window.onload = function (){
	/*-----------下拉菜单---------*/

	//1. 获取元素节点
	var currentAddr = document.getElementsByClassName('currentAddress')[0];
	var select = document.getElementsByClassName('select')[0];

	//获取内层列表中地址项
	var address = select.children;
	//为每一项添加点击事件
	for(var i = 0; i < address.length; i ++){
		address[i].onclick = function(){
			//传值
			currentAddr.innerHTML = this.innerHTML;
		};
	}

	/*-----------图片轮播-----------*/
	//1. 获取图片数组
	//2. 定时器实现图片切换
	//3. 图片切换主要切换数组下标，防止数组越界

	var banner = document.getElementsByClassName('wrapper')[0];
	var imgs = banner.children; //图片数组
	var imgNav = document.getElementsByClassName('imgNav')[0];
	var indInfo = imgNav.children; //索引数组
	var imgIndex = 0; //初始下标
	var timer;
	timer = setInterval(autoPlay,1000); //定时器
	function autoPlay(){
		//设置元素隐藏与显示
		imgs[imgIndex].style.display = "none";
		/*
		++ imgIndex;
		if(imgIndex == imgs.length){
			imgIndex = 0;
		}
		*/
		imgIndex = ++ imgIndex == imgs.length ? 0 : imgIndex;

		imgs[imgIndex].style.display = "block";

		for(var i = 0; i < indInfo.length; i ++){
			indInfo[i].style.background = "gray";
		}
		//切换索引 切换背景色
		indInfo[imgIndex].style.background = "red";
	}
	banner.onmouseover = function (){
		//停止定时器
		clearInterval(timer);
	};

	banner.onmouseout = function (){
		timer = setInterval(autoPlay,1000);
	};

};

function check_login() {
    //向/check_login/发送异步请求
    $.get('/check_login/', function (data) {
        var html = '';
        if (data.loginStatus === 0) {
            html += '<a href="/login">[登录]</a>';
            html += '<a href="/register">[注册，有惊喜]</a>';
        }
        else {
            html += '欢迎：' + data.uname;
            html += '<a href="/logout">[退出]</a>';
        }
        $('#login').html(html);
    }, 'json')
}

/* 加载所有的商品分类以及商品信息(每个分类取前10个) */
function loadGoods(){
    $.get('/load_goods_type/',function(data){
        //data 就是响应回来的JSON对象
        var show = '';
        $.each(data,function (i,obj) {
            //从Obj中取出type并转换为json对象
            var jsontype = JSON.parse(obj.type);
            //加载type信息
            show += '<div class="item" style="overflow: hidden;">';
            show += '<p class="goodsClass">';
            show += '<img src=" /'+ jsontype.picture +' "> ';
            show += '<a href="#">更多</a>';
            show += '</p>';
            //准备加载ul和li
            show += '<ul>';
            //从Obj中取出goods并转换为json对象
            var jsongoods = JSON.parse(obj.goods);
            $.each(jsongoods,function (i,good) {
                //创建li
                show += '<li ';
                if( (i+1)%5==0 ){
                    show += 'class="no-margin"';
                }
                show += '>';
                show += '<p>';
                show += '<img src="/' + good.fields.picture + '">';
                show += '</p>';
                show += '<div class="content">';
                show += '<a href="javascript:add_cart(' + good.pk + ');"><img src="/static/images/cart.png"></a>';
                show += '<p>' + good.fields.title + '</p>';
                show += '<span>' + '&yen;' + good.fields.price + '/' + good.fields.spec + '</span>';
                show += '</div>';
                show += '</li>';
            });
            show += '</ul>';
            show += '</div>';
        });
        $('#main').html(show);
    },'json');
}

/* 添加商品到购物车 */
function add_cart(good_id){
    //1.验证用户，如果没有用户登录则给出相应提示
    $.get('/check_login/',function (data) {
        if (data.loginStatus === 1){
            //保存商品至购物车
            var dic = {
                'id':good_id,
            };
            $.get('/add_cart/',dic,function (data) {
                if (data.status == 1) {
                    alert(data.statusText)
                }
            },'json');

        }
        else {
            alert('请先登录');
        }
    },'json')
}
$(function(){
    //调用check_login，检查登录状态
    check_login();
    //调用loadGoods函数得到所有的类型和商品
    loadGoods();

});


