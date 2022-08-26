from pickle import FALSE
from django.shortcuts import render,redirect
from .models import stock_item_crt,CreateStockGrp,group_summary,payhead_crt

# Create your views here.


def index(request):
    return render(request,'base.html')

def profit(request):
    return render(request,'profit.html') 


def stockgroup(request):
    std=CreateStockGrp.objects.all()
    return render(request,'stockgroup.html',{'std':std})

def item_list(request,pk):
    std=group_summary.objects.filter(CreateStockGrp_id=pk)
    return render(request,'items.html',{'std':std})  

def  payhead_list(request):
    std=payhead_crt.objects.all()
    return render(request,'payhead_items.html',{'std':std}) 


def stock_groups(request):
    und=CreateStockGrp.objects.all()
    if request.method=='POST':
        name=request.POST['name']
        alias=request.POST['alias']
        under_name=request.POST['under_name']
        quantities=request.POST['quantities']
        stockgrp=CreateStockGrp(name=name,alias=alias,under_name=under_name,quantities=quantities)
        stockgrp.save()
        return redirect('stock_items')
    return render(request,'group_stock.html',{'und':und})    



def stock_items(request):
    grp=CreateStockGrp.objects.all()
    if request.method=='POST':
        name=request.POST['name']
        alias=request.POST['alias']
        under=request.POST['under']
        grp1=CreateStockGrp.objects.get(id=under)
        # category=request.POST['category',FALSE]
        units=request.POST['units']
        batches=request.POST['batches']
        manufacturing_date=request.POST['manufacturing_date']
        expiry_dates=request.POST['expiry_dates']
        rate_of_duty=request.POST['rate_of_duty']
        quantity=request.POST['quantity']
        rate=request.POST['rate']
        per=request.POST['per']
        value=request.POST['value']
        additional=request.POST['additional']
        crt=group_summary(name=name,alias=alias,under=under,units=units,batches=batches,
                           manufacturing_date=manufacturing_date,expiry_dates=expiry_dates,
                           rate_of_duty=rate_of_duty,quantity=quantity,rate=rate,per=per,value=value,additional=additional,CreateStockGrp=grp1)
        crt.save()
        return redirect('stock_items')
    return render(request,'stockitem.html',{'grp':grp})


def payhead(request):
    # att=attendance_crt.objects.all()
    pay=payhead_crt.objects.all()
    if request.method=='POST':
        name=request.POST['name']
        alias=request.POST['alias']
        payhead_type=request.POST['payhead_type']
        under_name=request.POST['under_name']
        net_salary=request.POST['net_salary']
        pay_slip_name1=request.POST['pay_slip_name']
        currency_ledger=request.POST['currency_ledger']
        calculation_type=request.POST['calculation_type']
        attendance_type=request.POST['attendance_type']
        production_type=request.POST['production_type']
        crt=payhead_crt(name=name,alias=alias,payhead_type=payhead_type,under_name=under_name,net_salary=net_salary,pay_slip_name=pay_slip_name1,currency_ledger=currency_ledger,calculation_type=calculation_type
                        ,attendance_type=attendance_type,production_type=production_type)
        crt.save()
    return render(request,'payhead.html',{'pay':pay})

def ledger(request):
    return render(request,'ledger.html')
