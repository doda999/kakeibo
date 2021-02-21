from django.urls import path
from . import views

app_name = 'money'

urlpatterns = [
    path('<int:year>/<int:month>',views.List.as_view(),name='list'),
    path('expence/new',views.NewExpence.as_view(),name='new_expence'),
    path('expence/<int:pk>/update',views.ExpenceUpdate.as_view(),name='expence_update'),
    path('expence/<int:pk>/delete',views.DeleteExpence,name="expence_delete"),
    # path('expence/<int:year>/<int:month>/plot',views.expenceSvg,name='plot_expence'),
    path('revenue/new',views.NewRevenue.as_view(),name="new_revenue"),
    path('revenue/<int:pk>/update',views.RevenueUpdate.as_view(),name='revenue_update'),
    path('revenue/<int:pk>/delete',views.DeleteRevenue,name="revenue_delete"),
    # path('revenue/<int:year>/<int:month>/plot',views.revenueSvg,name='plot_revenue'),
]