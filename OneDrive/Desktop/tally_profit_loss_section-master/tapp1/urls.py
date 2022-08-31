from django .urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('profit',views.profit,name='profit'),
    path('stockgroup',views.stockgroup,name='stockgroup'),
    path('stock_item',views.stock_items,name='stock_items'),
    path('group',views.stock_groups,name="stock_groups"),
    path('payhead',views.payhead,name='payhead'),
    path('items/<int:pk>',views.item_list,name='item_list'),
    path('payhead_list',views.payhead_list,name='payhead_list'),
    path('ledger',views.ledger,name='ledger'),
    path('save_ledger',views.save_ledger,name='save_ledger'),
    path('sales',views.sales,name='sales'),
    path('indirect',views.indirect,name='indirect'),
  
]