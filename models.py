from django.db import models

# Create your models here.
class User(models.Model):
    uphone = models.CharField(max_length=11)
    upwd = models.CharField(max_length=12,verbose_name='密码')
    uname = models.CharField(max_length=30,verbose_name='用户名')
    uemail = models.EmailField(verbose_name='邮箱')
    isActive = models.BooleanField(default=True,verbose_name='激活用户')

    def __str__(self):
        return self.uname

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class GoodsType(models.Model):
    title = models.CharField(max_length=30,verbose_name='类型标题')
    picture = models.ImageField(upload_to='static/upload/goodstype',null=True,verbose_name='类型图片')
    desc = models.TextField(verbose_name='类型描述')

    def __str__(self):
        return self.title

    def to_dict(self):
        dic = {
            'title':self.title,
            'picture':self.picture.__str__(),
            'desc':self.desc,
        }
        return dic

    class Meta:
        db_table = 'goodstype'
        verbose_name = '商品类型'
        verbose_name_plural = verbose_name


class Goods(models.Model):
    title = models.CharField(max_length=40,verbose_name='商品名称')
    price = models.DecimalField(max_digits=7,decimal_places=2,verbose_name='商品价格')
    spec = models.CharField(max_length=20,verbose_name='商品规格')
    picture = models.ImageField(upload_to='static/upload/goods',verbose_name='商品图片')
    goodstype = models.ForeignKey(GoodsType,verbose_name='商品类型')
    isActive = models.BooleanField(default=True,verbose_name='是否上架')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'goods'
        verbose_name = '商品'
        verbose_name_plural = verbose_name


class CartInfo(models.Model):
    user = models.ForeignKey(User,verbose_name='用户')
    goods = models.ForeignKey(Goods,verbose_name='商品')
    count = models.IntegerField(verbose_name='数量')

    def __str__(self):
        return self.user.uname

    class Meta:
        db_table = 'cartinfo'
        verbose_name = '购物车'
        verbose_name_plural = verbose_name


