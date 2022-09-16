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
    path('grp_month/<int:pk>',views.grp_month,name='grp_month'),
    path('grp_month2/<int:pk>',views.grp_month_2,name='grp_month_2'),
    path('sales_month/<int:pk>',views.sales_month,name='sales_month'),
    path('sales_month2/<int:pk>',views.sales_month_2,name='sales_month_2'),
    path('payhead/<int:pk>',views.payhead_month,name='payhead_month'),
    path('stock_month/<int:pk>',views.stock_month,name='stock_month'),
    path('voucher/<int:pk>',views.pay_voucher,name='pay_voucher'),
    path('stock_voucher/<int:pk>',views.stock_voucher,name='stock_voucher'),
    path('purchase',views.purchase,name='purchase'),
    path('direct_exp',views.direct_exprenses,name='direct_exprenses'),
    path('indirect_exp',views.indirect_expenses,name='indirect_expenses'),
    path('stock_group2',views.stock_group2,name='stock_group2'),
    path('items_2/<int:pk>',views.items_2,name='items_2')
]