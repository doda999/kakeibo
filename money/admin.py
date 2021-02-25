from django.contrib import admin
from .models import Expence,Category_out,Revenue,Category_in

# Register your models here.
@admin.register(Expence)
class ExpenceAdmin(admin.ModelAdmin):
    # モデルのリストに表示される項目
    list_display = ('user','date','detail','cost','category')
    # n+1問題(負荷問題)の対策
    list_select_related = ('category','user')
    # 検索窓で検索できるもの
    search_fields = ('user__username','detail','date','category__name')
    # 並びかえ
    ordering =('user',)
    # フィルタ
    list_filter = ('detail', 'user', 'category', 'date')

@admin.register(Category_out)
class CategoryOutAdmin(admin.ModelAdmin):
    pass

@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    pass

@admin.register(Category_in)
class CategoryInAdmin(admin.ModelAdmin):
    pass
