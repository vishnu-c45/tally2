from django .urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('profit',views.profit,name='profit'),
    path('stockgroup',views.stockgroup,name='stockgroup'),
    path('stock_item',views.stock_items,name='stock_items'),
    path('group',views.stock_groups,name="stock_groups"),
    path('payhead',views.payhead,name='payhead'),
    path('items',views.item_list,name='item_list')
  
]