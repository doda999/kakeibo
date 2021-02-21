from django.db import models
from accounts.models import User

# Create your models here.
# 支出のカテゴリー
class Category_out(models.Model):
    # 文字を使う
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        unique=True
    )
    # categoryの名前を表す
    def __str__(self):
        return self.name

# 支出内容
class Expence(models.Model):
    money_cd = models.AutoField(primary_key=True)
    date = models.DateField(verbose_name='日付')
    detail = models.CharField(max_length=200,verbose_name='概要')
    cost = models.IntegerField(default=0,verbose_name='金額')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category_out, on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.detail+'¥'+str(self.cost)

# 収入のカテゴリー
class Category_in(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        unique=True
    )
    # categoryの名前を表す
    def __str__(self):
        return self.name

# 収入内容
class Revenue(models.Model):
    money_cd = models.AutoField(primary_key=True)
    date = models.DateField(verbose_name='日付')
    detail = models.CharField(max_length=200,verbose_name='概要')
    cost = models.IntegerField(default=0,verbose_name='金額')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category_in, on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.detail+'¥'+str(self.cost)

